import pytest
import json

from puzzlesolver.puzzles import Klotski
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *


def move(move0, move1):
    return (move0, move1)


# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    puzzle0 = Klotski.deserialize('10911991111111111991')
    puzzle1 = Klotski.deserialize('10911991111111111991')
    puzzle2 = Klotski.deserialize('11111991109119911111')
    puzzle3 = Klotski.deserialize('10911991111111111919')

    # Checks if two of the exact same states have the same hash
    assert hash(puzzle0) == hash(puzzle1)

    # Special case: It doesn't matter if the disks are on the left or middle rod. It's the same remoteness, so they should have the same hash
    # assert hash(puzzle0) == hash(puzzle2)

    # The start state should not have the same hash as the end state.
    assert hash(puzzle0) != hash(puzzle3)


def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ['10911991111111111991', '10911991111111111991', '10911991111111911911', '10911991111111111919', '11111991109119911111']

    for code in codes:
        puzzle = Klotski.deserialize(code)
        assert puzzle.serialize() == code


def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""

    # Expected primitive of start state should be UNDECIDED
    puzzle = Klotski.deserialize('11111991109119911111')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

    # Expected primitive of end state should be SOLVABLE
    puzzle = Klotski.deserialize('11111111199110911991')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE


def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""

    # Tests if state after move matches serialization
    puzzle0 = Klotski.deserialize('11111111109199911119')
    puzzle1 = puzzle0.doMove(move(14, 'r'))
    assert puzzle1.serialize() == '11111111109199911191'
    puzzle2 = puzzle1.doMove(move(12, 'u'))
    assert puzzle2.serialize() == '11111111109119919191'
    puzzle3 = puzzle2.doMove(move(13, 'l'))

    # Invalid moves raises an Exception
    with pytest.raises(Exception): puzzle1.doMove(move(0, 'd'))
    with pytest.raises(Exception): puzzle0.doMove(move(12, 'd'))
    with pytest.raises(Exception): puzzle0.doMove(move(11, 'r'))

    # Length of generated moves should match expected.
    assert len(puzzle0.generateMoves()) == 4
    assert len(puzzle1.generateMoves()) == 4
    assert len(puzzle2.generateMoves()) == 4
    assert len(puzzle3.generateMoves()) == 3

def testPositions():
    """Tests the default start state and finish positions matches the expected serializations."""

    # Default start
    puzzle0 = Klotski.generateStartPosition('1')
    assert puzzle0.serialize() == '10911991111111111991'

    # end
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 3
    print(puzzles)
    assert puzzles[0].serialize() == '11111111199110911991'


# def testValidation():
#     """Tests four different serializations and checks if it matches the expected response."""
#
#     # Four invalid serializations
#     invalid_puzzle = "1_2_3--"
#     valid_puzzle = "3_2_1--"
#     blank_puzzle = ""
#     weird_input = "123__"
#
#     # Four exceptions raised
#     pytest.raises(PuzzleException, Hanoi.validate, blank_puzzle, "3")
#     pytest.raises(PuzzleException, Hanoi.validate, weird_input, "3")
#     pytest.raises(PuzzleException, Hanoi.validate, invalid_puzzle, "3")
#     pytest.raises(PuzzleException, Hanoi.validate, valid_puzzle, "4")
#     Hanoi.validate(valid_puzzle, "3")


# Server methods
def testServerPuzzle(client):
    """Tests server functionality by trying out a series of inputs."""
    rv = client.get('/{}/'.format(Klotski.puzzleid))
    d = json.loads(rv.data)

    assert d['response']['variants'] == list(Klotski.variants.keys())

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness

    pid = Klotski.puzzleid
    helper(pid, '11111111199110911991', 1, 0)
    # helper(pid, '-1-', 1, 1)
    # helper(pid, '--1', 1, 0)
    #
    # helper(pid, '2_1-3-', 1, 4)