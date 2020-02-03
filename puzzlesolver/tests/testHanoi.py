import pytest

from ..puzzles.Hanoi import Hanoi
from ..solver.GeneralSolver import GeneralSolver
from ..util import *

def testGeneral():
    for i in range(10):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver()
        assert solver.solve(puzzle) == GameValue.WIN
        assert solver.getRemoteness(puzzle) == 2**i - 1
