
import pytest
import json

from puzzlesolver.puzzles import NQueens, PuzzleManager
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue, PuzzleException


# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    puzzle0 = NQueens.fromString('R_A_4_4_qqqq------------')
    puzzle1 = NQueens.fromString('R_A_4_4_qqqq------------')
    puzzle2 = NQueens.fromString('R_A_4_4_--------q----qqq')

    # Checks if two exact same puzzles have the same hash
    assert hash(puzzle0) == hash(puzzle1)

    # Checks is two different puzzles have different hash
    assert hash(puzzle0) != hash(puzzle2)


def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ['R_A_4_4_qq-q----q-------', 'R_A_4_4_qqqq------------', 'R_A_4_4_--------q----qqq', 'R_A_4_4_---q---q---q---q', 'R_A_4_4_----qq----qq----']

    for code in codes:
        puzzle = NQueens.fromString(code)
        assert puzzle.toString() == code


def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""

    # Expected primitive of start state should be UNDECIDED
    puzzle = NQueens.fromString('R_A_4_4_qqqq------------')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

    # Expected primitive of end state should be SOLVABLE
    puzzle = NQueens.fromString('R_A_4_4_--q-q------q-q--')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE


def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""

    # Tests if state after move matches serialization
    tests = [
        ('R_A_4_4_qqqq------------', {'M_0_12', 'M_1_11', 'M_3_13', 'M_3_14', 'M_3_8', 'M_2_5', 'M_2_7', 'M_2_12', 'M_0_4', 'M_0_13', 'M_1_12', 'M_0_7', 'M_1_7', 'M_0_14', 'M_3_15', 'M_1_13', 'M_3_9', 'M_1_8', 'M_3_5', 'M_0_11', 'M_1_14', 'M_2_15', 'M_3_6', 'M_1_6', 'M_0_8', 'M_0_5', 'M_2_11', 'M_1_10', 'M_0_6', 'M_2_13', 'M_0_9', 'M_3_10', 'M_1_4', 'M_3_7', 'M_3_11', 'M_3_12', 'M_0_15', 'M_2_14', 'M_0_10', 'M_2_6', 'M_1_5', 'M_1_15', 'M_1_9', 'M_2_4', 'M_2_8', 'M_3_4', 'M_2_10', 'M_2_9'}),
        ('R_A_4_4_----qqqq--------', {'M_4_12', 'M_6_1', 'M_4_11', 'M_7_1', 'M_7_11', 'M_6_2', 'M_4_3', 'M_6_12', 'M_4_0', 'M_5_1', 'M_4_10', 'M_6_9', 'M_6_11', 'M_5_15', 'M_7_14', 'M_6_15', 'M_5_2', 'M_4_1', 'M_6_10', 'M_5_10', 'M_6_13', 'M_7_13', 'M_6_8', 'M_4_8', 'M_5_3', 'M_7_3', 'M_7_2', 'M_7_8', 'M_4_9', 'M_6_0', 'M_7_9', 'M_7_12', 'M_7_15', 'M_5_9', 'M_5_13', 'M_4_2', 'M_7_10', 'M_6_14', 'M_5_12', 'M_5_0', 'M_5_14', 'M_4_14', 'M_7_0', 'M_5_8', 'M_4_15', 'M_4_13', 'M_6_3', 'M_5_11'}),
        ('R_A_4_4_-----q------qqq-', {'M_14_3', 'M_14_4', 'M_13_4', 'M_13_10', 'M_14_1', 'M_14_2', 'M_13_7', 'M_5_1', 'M_14_15', 'M_13_2', 'M_13_9', 'M_12_7', 'M_5_6', 'M_12_2', 'M_14_7', 'M_14_9', 'M_14_8', 'M_12_3', 'M_13_8', 'M_12_1', 'M_13_0', 'M_12_8', 'M_12_6', 'M_14_6', 'M_5_8', 'M_5_11', 'M_13_15', 'M_12_0', 'M_5_10', 'M_12_4', 'M_5_3', 'M_5_2', 'M_13_6', 'M_14_10', 'M_12_9', 'M_5_7', 'M_14_0', 'M_5_4', 'M_12_10', 'M_13_1', 'M_13_11', 'M_12_11', 'M_5_0', 'M_14_11', 'M_5_9', 'M_5_15', 'M_12_15', 'M_13_3'})
    ]

    for test in tests:
        puzzle = NQueens.fromString(test[0])
        moves = puzzle.generateMoves()
        print(moves)
        print(moves)
        assert moves == test[1]
        for move in moves:
            puzzle.doMove(move)


def testPositions():
    """Tests the default start state matches the expected serializations."""

    puzzle0 = NQueens.generateStartPosition('4')
    assert puzzle0.toString() == 'R_A_4_4_qqqq------------'


def testValidation():

    """4 invalid serializations"""
    tests = [
        ("", "4"),
        ("R_A_5_5_qqqqq-------------------", "5"),
        ("R_A_4_4_qqqqq--------------------", "4"),
        ("R_A_4_4_qqqq-------------", "4")
    ]
    for test in tests:
        pytest.raises(PuzzleException, PuzzleManager.validate, NQueens.id, test[1], test[0])


def testSolver():
    """Tests the solver functionality of the Puzzle"""

    puzzle = NQueens()
    solver = GeneralSolver(puzzle)
    solver.solve()

    assert solver.getRemoteness(NQueens.fromString('R_A_4_4_--q--q----q--q--')) == 2


def testServerPuzzle(client):
    """Tests server functionality by trying out a series of inputs."""
    rv = client.get('/{}/'.format(NQueens.id))
    d = json.loads(rv.data)

    for variant in d['response']["variants"]:
        assert variant['variantId'] in NQueens.variants

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness

    pid = NQueens.id
    helper(pid, 'R_A_4_4_--q-q------q-q--', "4", 0)
    helper(pid, 'R_A_4_4_--q-q-----q--q--', "4", 1)
    helper(pid, 'R_A_4_4_--q--q----q--q--', "4", 2)
    helper(pid, 'R_A_4_4_qq-qq-----------', "4", 3)
