import pytest
import tempfile

# Import server
import sys
sys.path.append("..")

import server

from puzzlesolver.util import PuzzleValue
from puzzlesolver.puzzles import GraphPuzzle

########################################################################
# Server Fixtures
########################################################################

@pytest.fixture
def client(tmpdir):
    app = server.app
    if app.config['TESTING'] != True:
        app.config['TESTING'] = True
        app.config['DATABASE_DIR'] = tmpdir

        server.init_data()

    with app.test_client() as client:
        yield client

@pytest.fixture
def simple():
    def helper(solver_cls, csp=False):
        forward = GraphPuzzle(0, csp=csp)
        bidirectional = GraphPuzzle(1, csp=csp)
        backward = GraphPuzzle(2, csp=csp)
        sol = GraphPuzzle(3, value=PuzzleValue.SOLVABLE, csp=csp)

        sol.setMove(forward, movetype="for")
        sol.setMove(bidirectional, movetype="bi")
        sol.setMove(backward, movetype="back")

        solver = solver_cls(sol)
        solver.solve()

        assert solver.getRemoteness(backward) == 1
        assert solver.getRemoteness(sol) == 0
        assert solver.getRemoteness(bidirectional) == 1
        assert solver.getRemoteness(forward) == PuzzleValue.UNSOLVABLE
    return helper
