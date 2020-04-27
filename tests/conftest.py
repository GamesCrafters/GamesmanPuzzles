import pytest
import tempfile

import puzzlesolver.solvers
from puzzlesolver.server import app
from puzzlesolver.puzzles import puzzleList, GraphPuzzle
from puzzlesolver.util import PuzzleValue

@pytest.fixture
def client(tmpdir):
    app.config['TESTING'] = True
    dir_path = tmpdir
    app.config['DATABASE_DIR'] = dir_path

    for p_cls in puzzleList.values():
        if hasattr(p_cls, 'test_variants'):
            variants = p_cls.test_variants
        else: 
            variants = p_cls.variants
        for variant in variants:
            s_cls = variants[variant]
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=dir_path)
            solver.solve()

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