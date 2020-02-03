import pytest

from ..puzzles.Hanoi import Hanoi
from ..solver.GeneralSolver import GeneralSolver
from ..util import *

def testGeneral():
    for i in range(10):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver()
        assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1
