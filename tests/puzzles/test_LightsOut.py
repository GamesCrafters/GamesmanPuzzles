import pytest
import json

from puzzlesolver.puzzles import LightsOut as p_cls
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue, PuzzleException


def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = [
        "R_A_2_2_----",
        "R_A_2_2_****",
        "R_A_3_3_---------",
        "R_A_3_3_*********",
        "R_A_3_3_****-**-*",
    ]

    for code in codes:
        puzzle = p_cls.fromString(code)
        assert puzzle.toString() == code


def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""

    # Expected primitive of start state should be UNDECIDED
    puzzle = p_cls.fromString("R_A_2_2_----")
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

    # Expected primitive of end state should be SOLVABLE
    puzzle = p_cls.fromString("R_A_2_2_****")
    assert puzzle.primitive() == PuzzleValue.SOLVABLE


def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""

    # Tests if state after move matches serialization
    tests = [
        ("R_A_2_2_----", {"A_1_0", "A_1_1", "A_1_2", "A_1_3"}),
        ("R_A_2_2_--*-", {"A_1_0", "A_1_1", "A_1_2", "A_1_3"}),
        ("R_A_2_2_****", {"A_1_0", "A_1_1", "A_1_2", "A_1_3"}),
        (
            "R_A_3_3_---------",
            {
                "A_1_0",
                "A_1_1",
                "A_1_2",
                "A_1_3",
                "A_1_4",
                "A_1_5",
                "A_1_6",
                "A_1_7",
                "A_1_8",
            },
        ),
    ]

    for test in tests:
        puzzle = p_cls.fromString(test[0])
        moves = set(puzzle.generateMoves())
        assert moves == test[1]
        for move in moves:
            puzzle.doMove(move)


def testPositions():
    """Tests the default start state and finish positions matches the expected serializations."""

    # Default start
    puzzle0 = p_cls.generateStartPosition("3")
    assert puzzle0.toString() == "R_A_3_3_---------"

    # Default end (only contains one end)
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].toString() == "R_A_3_3_*********"


def testValidation():
    """Tests four different serializations and checks if it matches the expected response."""

    # Four invalid serializations
    tests = [("", "3"), ("R_A_3_3_-*-*-*-*-", "2"), ("R_A_2_2_-*-*-*-*-", "3"), ("R_A_2_2_-*-*", "3")]

    for test in tests:
        try:
            PuzzleManager.validate(p_cls.id, test[1], test[0])
        except PuzzleException:
            pass
        else:
            print("Validation: {}".format(test))
            raise Exception


def testSolver():
    """Tests the solver functionality of the Puzzle"""

    puzzle = p_cls()
    solver = GeneralSolver(puzzle)
    solver.solve()

    assert solver.getRemoteness(p_cls.fromString("R_A_2_2_----")) == 4


# Server methods
def testServerPuzzle(client):
    """Tests server functionality by trying out a series of inputs."""
    rv = client.get("/{}/".format(p_cls.id))
    d = json.loads(rv.data)

    for variant in d["response"]["variants"]:
        print(d)
        assert variant["variantId"] in p_cls.variants

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get("/{}/{}/{}/".format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d["response"]["remoteness"] == remoteness

    pid = p_cls.id
    helper(pid, "R_A_2_2_----", "2", 4)
    helper(pid, "R_A_2_2_****", "2", 0)
    helper(pid, "R_A_2_2_*---", "2", 1)

    helper(pid, "R_A_3_3_-********", "3", 5)
