import pytest
import warnings

import tempfile

# Import server
import sys
sys.path.append("..")

from puzzlesolver.util import PuzzleValue
from puzzlesolver.puzzles import GraphPuzzle, PuzzleManager

########################################################################
# Server Fixtures
########################################################################

db_dir = None

@pytest.fixture
def database_dir(tmpdir):
    global db_dir
    if not db_dir is None:
        return db_dir
    for p_cls in PuzzleManager.getPuzzleClasses():
        variants = p_cls.test_variants
        if not variants: warnings.warn(UserWarning("{} does not have any test variants. It's correctness may vary.".format(p_cls.name)))
        for variant in variants:
            s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=tmpdir)
            solver.solve()
    db_dir = tmpdir
    return db_dir

@pytest.fixture
def client(database_dir):
    import server
    app = server.app
    if app.config['TESTING'] != True:
        app.config['TESTING'] = True
        app.config['DATABASE_DIR'] = database_dir

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
        assert solver.getRemoteness(forward) == PuzzleValue.MAX_REMOTENESS
    return helper
