import pytest

from puzzlesolver.puzzles.Hanoi import Hanoi
from puzzlesolver.solver.GeneralSolver import GeneralSolver
from puzzlesolver.util import *

def testGeneral():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver()
        assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1
