import pytest
import tempfile

from puzzlesolver import server
from puzzlesolver.util import PuzzleValue
from puzzlesolver.puzzles import puzzleList, GraphPuzzle

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
    def helper(solver_cls):
        forward = GraphPuzzle(0)
        bidirectional = GraphPuzzle(1)
        backward = GraphPuzzle(2)
        sol = GraphPuzzle(3, value=PuzzleValue.SOLVABLE)

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