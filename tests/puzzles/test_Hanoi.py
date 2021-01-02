import pytest
import json

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue, PuzzleException

def move(move0, move1):
    return (move0, move1)

# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    puzzle0 = Hanoi.deserialize('3_2_1--')
    puzzle1 = Hanoi.deserialize('3_2_1--')
    #puzzle2 = Hanoi.deserialize('-3_2_1-')
    puzzle3 = Hanoi.deserialize('--3_2_1')
    
    # Checks if two of the exact same states have the same hash
    assert hash(puzzle0) == hash(puzzle1)
    
    # Special case: It doesn't matter if the disks are on the left or middle rod. It's the same remoteness, so they should have the same hash
    #assert hash(puzzle0) == hash(puzzle2)
    
    # The start state should not have the same hash as the end state.
    assert hash(puzzle0) != hash(puzzle3)

def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ['3_2_1--', '-3_2_1-', '--3_2_1', '-3_2-1', '1--']
    
    for code in codes:
        puzzle = Hanoi.deserialize(code)
        assert puzzle.serialize() == code

def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""
    
    # Expected primitive of start state should be UNDECIDED
    puzzle = Hanoi.deserialize('3_2_1--')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    
    # Expected primitive of end state should be SOLVABLE
    puzzle = Hanoi.deserialize('--3_2_1')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE

def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""
    
    # Tests if state after move matches serialization
    puzzle0 = Hanoi.deserialize('3_2_1--')
    puzzle1 = puzzle0.doMove(move(0, 1))
    assert puzzle1.serialize() == '3_2-1-'
    puzzle2 = puzzle1.doMove(move(0, 2))
    assert puzzle2.serialize() == '3-1-2'
    
    puzzle3 = puzzle1.doMove(move(1, 0))
    assert puzzle0.serialize() == puzzle3.serialize()

    # Invalid moves raises an Exception
    with pytest.raises(Exception): puzzle1.doMove(move(0, 1))
    with pytest.raises(Exception): puzzle0.doMove(move(1, 0))
    with pytest.raises(Exception): puzzle0.doMove(move(0, 3))

    # Length of generated moves should match expected.
    assert len(puzzle0.generateMoves()) == 2
    assert len(puzzle1.generateMoves()) == 3
    assert len(puzzle2.generateMoves()) == 3
    assert len(puzzle3.generateMoves()) == 2

def testPositions():
    """Tests the default start state and finish positions matches the expected serializations."""
    
    # Default start
    puzzle0 = Hanoi.generateStartPosition('3')
    assert puzzle0.serialize() == '3_2_1--'
    
    # Default end (only contains one end)
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].serialize() == '--3_2_1'

def testValidation():
    """Tests four different serializations and checks if it matches the expected response."""
    
    # Four invalid serializations
    invalid_puzzle = "1_2_3--"
    valid_puzzle = "3_2_1--"
    blank_puzzle = ""
    weird_input = "123__"
    
    # Four exceptions raised
    pytest.raises(PuzzleException, Hanoi.validate, blank_puzzle, "3")
    pytest.raises(PuzzleException, Hanoi.validate, weird_input, "3")
    pytest.raises(PuzzleException, Hanoi.validate, invalid_puzzle, "3")
    pytest.raises(PuzzleException, Hanoi.validate, valid_puzzle, "4")
    Hanoi.validate(valid_puzzle, "3")

# Server methods
def testServerPuzzle(client):
    """Tests server functionality by trying out a series of inputs."""
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
