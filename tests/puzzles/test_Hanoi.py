import pytest
import json

from puzzlesolver.puzzles import Hanoi, PuzzleManager
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue, PuzzleException

def move(move0, move1):
    return (move0, move1)

# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    puzzle0 = Hanoi.fromString('7-0-0')
    puzzle1 = Hanoi.fromString('7-0-0')
    puzzle3 = Hanoi.fromString('0-0-7')
    
    # Checks if two of the exact same states have the same hash
    assert hash(puzzle0) == hash(puzzle1)
    
    # Special case: It doesn't matter if the disks are on the left or middle rod. It's the same remoteness, so they should have the same hash
    #assert hash(puzzle0) == hash(puzzle2)
    
    # The start state should not have the same hash as the end state.
    assert hash(puzzle0) != hash(puzzle3)

def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ['7-0-0', '0-7-0', '0-0-7', '6-1-0', '1-0-0']
    
    for code in codes:
        puzzle = Hanoi.fromString(code)
        assert puzzle.toString() == code

def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""
    
    # Expected primitive of start state should be UNDECIDED
    puzzle = Hanoi.fromString('7-0-0')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    
    # Expected primitive of end state should be SOLVABLE
    puzzle = Hanoi.fromString('0-0-7')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE

def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""
    
    # Tests if state after move matches serialization
    tests = [
        ('7-0-0', {(0, 1), (0, 2)}),
        ('0-7-0', {(1, 0), (1, 2)}),
        ('0-2-5', {(1, 0), (2, 1), (2, 0)}),
        ('1-2-4', {(0, 1), (0, 2), (1, 2)})
    ]

    for test in tests:
        puzzle = Hanoi.fromString(test[0])
        moves = set(puzzle.generateMoves())
        assert moves == test[1]
        for move in moves:
            puzzle.doMove(move)

def testPositions():
    """Tests the default start state and finish positions matches the expected serializations."""
    
    # Default start
    puzzle0 = Hanoi.generateStartPosition('3_3')
    assert puzzle0.toString() == '7-0-0'
    
    # Default end (only contains one end)
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].toString() == '0-0-7'

def testValidation():
    """Tests four different serializations and checks if it matches the expected response."""
    
    # Four invalid serializations
    tests = [
        ("", "3_3"),
        ("15-0-0", "4_3"),
        ("7-0-0", "3_4"),
        ("7-0-0-", "3_3")
    ]
    
    for test in tests:
        positionid = test[1]
        variantid = test[0]
        pytest.raises(
            PuzzleException, PuzzleManager.validate, 
            Hanoi.id, test[1], test[0])
    PuzzleManager.validate(Hanoi.id, "3_3", "7-0-0")
    
def testSolver():
    """Tests the solver functionality of the Puzzle"""

    puzzle = Hanoi()
    solver = GeneralSolver(puzzle)
    solver.solve()

    assert solver.getRemoteness(Hanoi.fromString('7-0-0')) == 7

# Server methods
def testServerPuzzle(client):
    """Tests server functionality by trying out a series of inputs."""
    rv = client.get('/{}/'.format(Hanoi.id))
    d = json.loads(rv.data)

    for variant in d['response']["variants"]:
        assert variant['variantId'] in Hanoi.variants

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    pid = Hanoi.id
    helper(pid, '1-0-0', "3_1", 1)
    helper(pid, '0-1-0', "3_1", 1)    
    helper(pid, '0-0-1', "3_1", 0)

    helper(pid, '3-4-0', "3_3", 4)
