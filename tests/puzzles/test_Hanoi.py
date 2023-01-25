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
    puzzle0 = Hanoi.fromString("R_A_3_3_A--B--C--")
    puzzle1 = Hanoi.fromString("R_A_3_3_A--B--C--")
    puzzle3 = Hanoi.fromString("R_A_3_3_--A--B--C")

    # Checks if two of the exact same states have the same hash
    assert hash(puzzle0) == hash(puzzle1)

    # The start state should not have the same hash as the end state.
    assert hash(puzzle0) != hash(puzzle3)


def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ["R_A_3_3_A--B--C--", "R_A_3_3_-A--B--C-", "R_A_3_3_--A--B--C", "R_A_3_3_---B--CA-"] 

    for code in codes:
        puzzle = Hanoi.fromString(code)
        assert puzzle.toString() == code


def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""

    # Expected primitive of start state should be UNDECIDED
    puzzle = Hanoi.fromString("R_A_3_3_A--B--C--")
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

    # Expected primitive of end state should be SOLVABLE
    puzzle = Hanoi.fromString("R_A_3_3_--A--B--C")
    assert puzzle.primitive() == PuzzleValue.SOLVABLE


def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""

    # Tests if state after move matches serialization
    tests = [
        ("R_A_3_3_A--B--C--", {"M_0_7", "M_0_8"}),
        ("R_A_3_3_-A--B--C-", {"M_1_6", "M_1_8"}),
        ("R_A_3_3_-----A-BC", {"M_7_6", "M_5_4", "M_5_6"}),
        ("R_A_3_3_------ABC", {"M_6_4", "M_6_5", "M_7_5"}),
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
    puzzle0 = Hanoi.generateStartPosition("3_3")
    assert puzzle0.toString() == "R_A_3_3_A--B--C--"

    # Default end (only contains one end)
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].toString() == "R_A_3_3_--A--B--C"


def testValidation():
    """Tests four different serializations and checks if it matches the expected response."""

    # Four invalid serializations
    tests = [("R_A_3_3_", "3_3"), ("R_A_4_3_A--B--C--D--", "4_3"), ("R_A_3_4_A--B--C--", "3_4"), ("R_A_3_3_A--B--C---", "3_3")]

    for test in tests:
        pytest.raises(
            PuzzleException, PuzzleManager.validate, Hanoi.id, test[1], test[0]
        )
    PuzzleManager.validate(Hanoi.id, "3_3", "R_A_3_3_A--B--C--")


def testSolver():
    """Tests the solver functionality of the Puzzle"""

    puzzle = Hanoi()
    solver = GeneralSolver(puzzle)
    solver.solve()

    assert solver.getRemoteness(Hanoi.fromString("R_A_3_3_A--B--C--")) == 7


# Server methods
# # def testServerPuzzle(client):
# #     """Tests server functionality by trying out a series of inputs."""
# #     rv = client.get("/{}/".format(Hanoi.id))
# #     d = json.loads(rv.data)
# #
# #     for variant in d["response"]["variants"]:
# #         assert variant["variantId"] in Hanoi.variants
# #
# #     def helper(puzzleid, code, variantid, remoteness):
# #         rv = client.get("/{}/{}/{}/".format(puzzleid, variantid, code))
# #         d = json.loads(rv.data)
# #         assert d["response"]["remoteness"] == remoteness
#
#     pid = Hanoi.id
#     helper(pid, "R_A_3_1_------A--", "3_1", 1)
#     helper(pid, "R_A_3_1_-------A-", "3_1", 1)
#     helper(pid, "R_A_3_1_--------A", "3_1", 0)
#
#     helper(pid, "R_A_3_3_---A--BC-", "3_3", 4)
