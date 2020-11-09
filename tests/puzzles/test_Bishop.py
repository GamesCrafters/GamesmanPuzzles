import pytest
import json

from puzzlesolver.puzzles import Bishop
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    # Note: Hash comparison between different sized boards is undefined
    puzzle0 = Bishop.deserialize('2_5_a1-c1_a5-c5')
    puzzle1 = Bishop.deserialize('2_5_a1-c1_a5-c5')
    puzzle2 = Bishop.deserialize('2_5_a5-c5_a1-c1')
    
    # Checks if two of the exact same states have the same hash
    assert hash(puzzle0) == hash(puzzle1)
    
    # The start state should not have the same hash as the end state.
    assert hash(puzzle0) != hash(puzzle2)

def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ['2_5_a1-c1_a5-c5', '2_5_a1-b2_b4-a5', '2_5_a3-c5_a1-c3', '3_7_a1-c1-e1_a7-c7-e7', '3_7_a1-c1-b2_b4-a5-a7']
    
    for code in codes:
        puzzle = Bishop.deserialize(code)
        assert puzzle.serialize() == code

def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""
    
    # Expected primitive of start state should be UNDECIDED
    puzzle = Bishop.deserialize('2_5_a1-c1_a5-c5')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    
    # Expected primitive of end state should be SOLVABLE
    puzzle = Bishop.deserialize('2_5_a5-c5_a1-c1')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE

def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""
    
    # Tests if state after move matches serialization
    puzzle0 = Bishop.deserialize('2_5_a1-c1_a5-c5')
    puzzle1 = puzzle0.doMove(('c5', 'b4'))
    assert puzzle1.serialize() == '2_5_a1-c1_b4-a5'
    puzzle2 = puzzle1.doMove(('c1', 'b2'))
    assert puzzle2.serialize() == '2_5_a1-b2_b4-a5'
    
    puzzle3 = puzzle1.doMove(('b4', 'c5'))
    assert puzzle0.serialize() == puzzle3.serialize()

    # Invalid moves raises an Exception
    with pytest.raises(Exception): puzzle1.doMove(('c5', 'b4'))
    with pytest.raises(Exception): puzzle0.doMove(('a1', 'b1'))
    with pytest.raises(Exception): puzzle0.doMove(('a1', 'd4'))
    with pytest.raises(Exception): puzzle0.doMove(('a1', 'e5'))

    # Length of generated moves should match expected.
    assert len(puzzle0.generateMoves()) == 4
    assert len(puzzle1.generateMoves()) == 4
    assert len(puzzle2.generateMoves()) == 4
    assert len(puzzle3.generateMoves()) == 4

def testPositions():
    """Tests the default start state and finish positions matches the expected serializations."""
    
    # Default start
    puzzle0 = Bishop.generateStartPosition('2x5')
    assert puzzle0.serialize() == '2_5_a1-c1_a5-c5'
    
    # Default end
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].serialize() == '2_5_a5-c5_a1-c1'

def testValidation():
    """Tests four different serializations and checks if it matches the expected response."""
    
    # Four invalid serializations
    invalid_puzzle = '2_5_a5_a1-c1'
    valid_puzzle = '2_5_a5-c5_a1-c1'
    blank_puzzle = ""
    weird_input = "2-5-a1_c1-a5_c5"
    
    # Four exceptions raised
    pytest.raises(PuzzleException, Bishop.validate, blank_puzzle, "2x5")
    pytest.raises(PuzzleException, Bishop.validate, weird_input, "2x5")
    pytest.raises(PuzzleException, Bishop.validate, invalid_puzzle, "2x5")
    pytest.raises(PuzzleException, Bishop.validate, valid_puzzle, "3x7")
    Bishop.validate(valid_puzzle, "2x5")

# Server methods
def testServerPuzzle(client):
    """Tests server functionality by trying out a series of inputs."""
    rv = client.get('/{}/'.format(Bishop.puzzleid))
    d = json.loads(rv.data)

    assert d['response']['variants'] == list(Bishop.variants.keys())

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    pid = Bishop.puzzleid
    helper(pid, '2_5_a1-c1_a5-c5', '2x5', 18)
    helper(pid, '2_5_a1-b2_a5-c5', '2x5', 17)    
    helper(pid, '2_5_a5-c5_a1-c1', '2x5', 0)

