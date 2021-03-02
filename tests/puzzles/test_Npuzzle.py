import pytest

from puzzlesolver.puzzles import Npuzzle, PuzzleManager
from puzzlesolver.solvers import GeneralSolver, sqlitesolver

from puzzlesolver.util import PuzzleValue, PuzzleException

def testRemotenessSanity():
    for i in range(2,3):
        puzzle = Npuzzle(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        assert solver.getValue(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 1

def testSerialization():
    for i in range(2,3):
        puzzle = Npuzzle(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        new_puzzle = Npuzzle.deserialize(puzzle.serialize())
        assert hash(puzzle) == hash(new_puzzle)

def testValidation():

    tests = [
        ("", "2"),
        ("123---", "2"),
        ("1-2-3-3", "2"),
        ("1-2-3-0", "3")
    ]
    for test in tests:
        pytest.raises(PuzzleException, PuzzleManager.validate, Npuzzle.puzzleid, test[1], test[0])

    PuzzleManager.validate(Npuzzle.puzzleid, "2", "1-2-3-0")