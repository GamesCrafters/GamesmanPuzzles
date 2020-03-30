import pytest

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def testGeneral():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        assert solver.getValue(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1
