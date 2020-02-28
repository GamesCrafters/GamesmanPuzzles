import pytest

from puzzlesolver.puzzles.graphpuzzle import GraphPuzzle
from puzzlesolver.solver.GeneralSolver import GeneralSolver
from puzzlesolver.util import *

@GraphPuzzle.variant_test
def testSimple():
    forward = GraphPuzzle(name="f")
    bi = GraphPuzzle(name="b")
    undo = GraphPuzzle(name="u")
    sol = GraphPuzzle(name="s", forwardChildren=[forward], biChildren=[bi], undoChildren=[undo], primitive=PuzzleValue.SOLVABLE)

    solver = GeneralSolver()
    solver.solve(sol)
    assert solver.getRemoteness(undo) == 1
    assert solver.getRemoteness(sol) == 0
    assert solver.getRemoteness(bi) == 1
    assert solver.getRemoteness(forward) == PuzzleValue.UNSOLVABLE
