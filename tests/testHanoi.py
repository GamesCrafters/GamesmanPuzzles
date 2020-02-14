import pytest

from puzzlesolver.puzzles.Hanoi import Hanoi
from puzzlesolver.solver.PickleSolverWrapper import PickleSolverWrapper
from puzzlesolver.util import *

def testGeneral():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = PickleSolverWrapper()
        assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1
