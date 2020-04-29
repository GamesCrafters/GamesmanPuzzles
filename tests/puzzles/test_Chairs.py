import pytest
import json

from puzzlesolver.puzzles import Chairs
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

# Unit testing
def testHash():
    puzzle0 = Chairs.deserialize('xxxxx-ooooo')
    puzzle1 = Chairs.deserialize('xxxxx-ooooo')
    puzzle2 = Chairs.deserialize('ooxxx-oxxoo')
    puzzle3 = Chairs.deserialize('oo-xxxoxxoo')
    assert hash(puzzle0) == hash(puzzle1)
    #assert hash(puzzle0) == hash(puzzle2)
    assert hash(puzzle0) != hash(puzzle3)

def testSerialization():
    codes = ['ooxxx-oxxoo', '-ooxxxoxxoo', 'ooooo-xxxxx', 'xxxxxooo-oo', 'xxx-xxoxoooo']
    for code in codes:
        puzzle = Chairs.deserialize(code)
        assert puzzle.serialize() == code

def testPrimitive():
    puzzle = Chairs.deserialize('ooooo-xxxxx')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE
    puzzle = Chairs.deserialize('xxxxx-ooooo')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    puzzle = Chairs.deserialize('ooooox-xxxx')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

def testMoves():
    puzzle0 = Chairs.deserialize('xxxxx-ooooo')
    puzzle1 = puzzle0.doMove(4)
    assert puzzle1.serialize() == 'xxxx-xooooo'
    puzzle2 = puzzle1.doMove(6)
    assert puzzle2.serialize() == 'xxxxox-oooo'
    puzzle3 = puzzle2.doMove(5)
    assert puzzle3.serialize() == 'xxxxo-xoooo'

    with pytest.raises(Exception): puzzle1.doMove(11)
    with pytest.raises(Exception): puzzle0.doMove(2)
    with pytest.raises(Exception): puzzle0.doMove(8)
    with pytest.raises(Exception): puzzle0.doMove(-1)

    assert len(puzzle0.generateMoves(movetype='for')) == 4
    assert len(puzzle1.generateMoves(movetype='for')) == 3
    assert len(puzzle2.generateMoves(movetype='for')) == 3
    assert len(puzzle3.generateMoves(movetype='for')) == 2

def testPositions():
    puzzle0 = Chairs.generateStartPosition('10')
    assert puzzle0.serialize() == 'xxxxx-ooooo'
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1

def testValidation():
    invalid_puzzle = 'xxxoo-ooooo'
    valid_puzzle = 'oooxx-ooxxx'
    blank_puzzle = ""
    weird_input = 'xxxyx_ooo--oo'
    pytest.raises(PuzzleException, Chairs.validate, blank_puzzle, "10")
    pytest.raises(PuzzleException, Chairs.validate, weird_input, "10")
    pytest.raises(PuzzleException, Chairs.validate, invalid_puzzle, "10")
    Chairs.validate(valid_puzzle, "10")

