import pytest

from puzzlesolver.puzzles import Npuzzle
from puzzlesolver.solvers import GeneralSolver, sqlitesolver

from puzzlesolver.util import PuzzleValue, PuzzleException

def testRemotenessSanity():
    for i in range(2,4):
        puzzle = Npuzzle(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        assert solver.getValue(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 1

def testSerialization():
    for i in range(2,4):
        puzzle = Npuzzle(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        new_puzzle = Npuzzle.deserialize(puzzle.serialize())
        assert hash(puzzle) == hash(new_puzzle)

def testValidation():
    invalid_puzzle = "1-2-3-3"
    valid_puzzle = "1-2-3-0"
    blank_puzzle = ""
    weird_input = "123---"
    pytest.raises(PuzzleException, Npuzzle.validate, blank_puzzle, "2")
    pytest.raises(PuzzleException, Npuzzle.validate, weird_input, "2")
    pytest.raises(PuzzleException, Npuzzle.validate, invalid_puzzle, "2")
    pytest.raises(PuzzleException, Npuzzle.validate, valid_puzzle, "3")
    Npuzzle.validate(valid_puzzle, "2")

    
