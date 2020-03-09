import pytest

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def testGeneral():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1
