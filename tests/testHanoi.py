import pytest

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solver import PickleSolverWrapper
from puzzlesolver.solver import GeneralSolver
from puzzlesolver.util import *

import tempfile

def testGeneral():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1

def testPickleWrapper():
    for i in range(5):
        with tempfile.TemporaryDirectory() as directory:
            puzzle = Hanoi(size=i)
            solver = PickleSolverWrapper(puzzle=puzzle, path=directory)
            assert not solver.values and not solver.remoteness
            assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
            assert solver.getRemoteness(puzzle) == 2**i - 1
            assert solver.values and solver.remoteness

            puzzle = Hanoi(size=i)
            solver = PickleSolverWrapper(puzzle=puzzle, path=directory)
            assert solver.values and solver.remoteness
            assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
            assert solver.getRemoteness(puzzle) == 2**i - 1