import pytest

from puzzlesolver.solvers import SqliteSolver
from puzzlesolver.puzzles import GraphPuzzle
from puzzlesolver.util import PuzzleValue

def test_simple(tmpdir):
    forward = GraphPuzzle(0)
    bidirectional = GraphPuzzle(1)
    backward = GraphPuzzle(2)
    sol = GraphPuzzle(3, value=PuzzleValue.SOLVABLE)

    sol.setMove(forward, movetype="for")
    sol.setMove(bidirectional, movetype="bi")
    sol.setMove(backward, movetype="back")

    solver = SqliteSolver(sol, dir_path=tmpdir)
    solver.solve()

    assert solver.getRemoteness(backward) == 1
    assert solver.getRemoteness(sol) == 0
    assert solver.getRemoteness(bidirectional) == 1
    assert solver.getRemoteness(forward) == PuzzleValue.UNSOLVABLE