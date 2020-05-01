import pytest
import json

from puzzlesolver.puzzles import Peg
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def move(move0, move1):
    return [move0, move1]

# Unit testing
def testHash():
    puzzle0 = Peg.deserialize('1_11_010_1111_01101_')
    puzzle1 = Peg.deserialize('1_11_010_1111_01101_')
    puzzle2 = Peg.deserialize('1_11_100_0011_11110_')
    puzzle3 = Peg.deserialize('0_10_100_1101_10111_')
    assert hash(puzzle0) == hash(puzzle1)
    #assert hash(puzzle0) == hash(puzzle2)
    assert hash(puzzle0) != hash(puzzle3)

def testSerialization():
    codes = ['1_11_010_1111_01101_', '1_11_110_0000_01101_', '0_00_010_0000_00000_', '1_11_110_0011_00011_', '0_11_111_1111_00001_']
    for code in codes:
        puzzle = Peg.deserialize(code)
        assert puzzle.serialize() == code

def testPrimitive():
    puzzle = Peg.deserialize('1_11_010_1111_01101_')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    puzzle = Peg.deserialize('0_00_000_1000_00000_')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE
    puzzle = Peg.deserialize('0_00_000_0000_00010_')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE
    puzzle = Peg.deserialize('0_10_000_0000_00010_')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

def testMoves():
    puzzle0 = Peg.deserialize('0_11_111_1111_11111_')
    puzzle1 = puzzle0.doMove(move([2,0],[0,0]))
    assert puzzle1.serialize() == '1_01_011_1111_11111_'
    puzzle2 = puzzle1.doMove(move([2,2],[2,0]))
    assert puzzle2.serialize() == '1_01_100_1111_11111_'
    puzzle3 = puzzle2.doMove(move([3,0],[1,0]))
    assert puzzle3.serialize() == '1_11_000_0111_11111_'

    with pytest.raises(Exception): puzzle1.doMove(move([1,0], [1,1]))
    with pytest.raises(Exception): puzzle0.doMove(move([0,0], [1,0]))
    with pytest.raises(Exception): puzzle0.doMove(move([3,0], [0,0]))

    assert len(puzzle0.generateMoves(movetype='for')) == 2
    assert len(puzzle1.generateMoves(movetype='for')) == 4
    assert len(puzzle2.generateMoves(movetype='for')) == 6
    assert len(puzzle3.generateMoves(movetype='for')) == 8

def testPositions():
    puzzle0 = Peg.generateStartPosition('Triangle')
    assert puzzle0.serialize() == '0_11_111_1111_11111_'
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 15

def testValidation():
    invalid_puzzle = '1_11_111_1111_11111_'
    valid_puzzle = '1_11_000_0111_11111_'
    blank_puzzle = ""
    weird_input = "111_0_11_22_22_11011"
    pytest.raises(PuzzleException, Peg.validate, blank_puzzle, "Triangle")
    pytest.raises(PuzzleException, Peg.validate, weird_input, "Triangle")
    pytest.raises(PuzzleException, Peg.validate, invalid_puzzle, "Triangle")
    Peg.validate(valid_puzzle, "Triangle")

def testPuzzleServer(client):
    pid = Peg.puzzleid
    rv = client.get('/{}/'.format(pid))
    d = json.loads(rv.data)

    assert d['response']['variants'] == list(Peg.variants.keys())

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    helper(pid, '0_00_000_0000_10000_', 'Triangle', 0)
    helper(pid, '0_00_000_0000_01100_', 'Triangle', 1)    
    helper(pid, '1_00_000_0000_00000_', 'Triangle', 0)
    helper(pid, '1_00_000_0000_10000_', 'Triangle', PuzzleValue.UNSOLVABLE)

    helper(pid, '1_11_000_0111_11111_', 'Triangle', 10)