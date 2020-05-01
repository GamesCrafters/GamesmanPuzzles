import pytest
import json

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def move(move0, move1):
    return (move0, move1)

# Unit testing
def testHash():
    puzzle0 = Hanoi.deserialize('3_2_1--')
    puzzle1 = Hanoi.deserialize('3_2_1--')
    puzzle2 = Hanoi.deserialize('-3_2_1-')
    puzzle3 = Hanoi.deserialize('--3_2_1')
    assert hash(puzzle0) == hash(puzzle1)
    #assert hash(puzzle0) == hash(puzzle2)
    assert hash(puzzle0) != hash(puzzle3)

def testSerialization():
    codes = ['3_2_1--', '-3_2_1-', '--3_2_1', '-3_2-1', '1--']
    
    for code in codes:
        puzzle = Hanoi.deserialize(code)
        assert puzzle.serialize() == code

def testPrimitive():
    puzzle = Hanoi.deserialize('3_2_1--')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    puzzle = Hanoi.deserialize('--3_2_1')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE

def testMoves():
    puzzle0 = Hanoi.deserialize('3_2_1--')
    puzzle1 = puzzle0.doMove(move(0, 1))
    assert puzzle1.serialize() == '3_2-1-'
    puzzle2 = puzzle1.doMove(move(0, 2))
    assert puzzle2.serialize() == '3-1-2'
    
    puzzle3 = puzzle1.doMove(move(1, 0))
    assert puzzle0.serialize() == puzzle3.serialize()

    with pytest.raises(Exception): puzzle1.doMove(move(0, 1))
    with pytest.raises(Exception): puzzle0.doMove(move(1, 0))
    with pytest.raises(Exception): puzzle0.doMove(move(0, 3))

    assert len(puzzle0.generateMoves()) == 2
    assert len(puzzle1.generateMoves()) == 3
    assert len(puzzle2.generateMoves()) == 3
    assert len(puzzle3.generateMoves()) == 2

def testPositions():
    puzzle0 = Hanoi.generateStartPosition('3')
    assert puzzle0.serialize() == '3_2_1--'
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].serialize() == '--3_2_1'

def testValidation():
    invalid_puzzle = "1_2_3--"
    valid_puzzle = "3_2_1--"
    blank_puzzle = ""
    weird_input = "123__"
    pytest.raises(PuzzleException, Hanoi.validate, blank_puzzle, "3")
    pytest.raises(PuzzleException, Hanoi.validate, weird_input, "3")
    pytest.raises(PuzzleException, Hanoi.validate, invalid_puzzle, "3")
    pytest.raises(PuzzleException, Hanoi.validate, valid_puzzle, "4")
    Hanoi.validate(valid_puzzle, "3")

# Server methods
def test_server_puzzle(client):
    rv = client.get('/{}/'.format(Hanoi.puzzleid))
    d = json.loads(rv.data)

    assert d['response']['variants'] == list(Hanoi.variants.keys())

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    pid = Hanoi.puzzleid
    helper(pid, '1--', 1, 1)
    helper(pid, '-1-', 1, 1)    
    helper(pid, '--1', 1, 0)

    helper(pid, '2_1-3-', 3, 4)