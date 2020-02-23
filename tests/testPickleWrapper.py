import pytest

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solvers import PickleSolverWrapper
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

import tempfile

from unittest import mock

import sys

class PickableMock(mock.Mock):
    def __reduce__(self):
        return (mock.Mock, ())

def testPickleWrapperGeneral():
    for i in range(1,5):
        with tempfile.TemporaryDirectory() as directory:
            puzzle = Hanoi(size=i)
            solver = PickleSolverWrapper(puzzle=puzzle, path=directory, solver=GeneralSolver())
            assert solver.solve(puzzle) == PuzzleValue.SOLVABLE
            assert solver.getRemoteness(puzzle) == 2**i - 1

def testPickleWrapper():
    with tempfile.TemporaryDirectory() as directory:
        solver_mock = PickableMock(spec=GeneralSolver)
        solver_mock.return_value.solve.return_value = True
        solver_mock.return_value.getRemoteness.return_value = -1

        solver = PickleSolverWrapper(Hanoi(), path=directory, solver=solver_mock)

        assert solver.solve() == solver_mock.solve()
        assert solver.getRemoteness() == solver_mock.getRemoteness()

def testPickleWrapperPersistence():
    open_mock = mock.mock_open()
    with mock.patch('__main__.open', open_mock, create=True):
        pickle_mock = mock.Mock()

        solver_mock = mock.Mock(spec=GeneralSolver)
        solver_mock.solve.return_value = True
        solver_mock.getRemoteness.return_value = -1

        pickle_mock.load.return_value = solver_mock
        with mock.patch('puzzlesolver.solvers.picklesolverwrapper.pickle', pickle_mock):
            solver = PickleSolverWrapper(Hanoi(), solver=None)

    pickle_mock.load.assert_called_once()
    assert solver.solve() == solver_mock.solve()
    assert solver.getRemoteness() == solver_mock.getRemoteness()