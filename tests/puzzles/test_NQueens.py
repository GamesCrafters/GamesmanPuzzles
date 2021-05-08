
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
    puzzle = NQueens.fromString('R_A_4_4_----------------')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

    # Expected primitive of end state should be SOLVABLE
    puzzle = NQueens.fromString('R_A_4_4_--q-q------q-q--')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE


def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""

    # Tests if state after move matches serialization
    tests = [
        ('R_A_4_4_----------------', {'A_q_0', 'A_q_3', 'A_q_4', 'A_q_2', 'A_q_15', 'A_q_12', 'A_q_8', 'A_q_13', 'A_q_14', 'A_q_5', 'A_q_10', 'A_q_7', 'A_q_6', 'A_q_11', 'A_q_9', 'A_q_1'}),
        ('R_A_4_4_-----q----------', {'A_q_8', 'A_q_7', 'A_q_13', 'A_q_15', 'A_q_3', 'A_q_6', 'A_q_2', 'A_q_10', 'A_q_4', 'A_q_0', 'A_q_1', 'A_q_11', 'A_q_12', 'A_q_14', 'A_q_9'}),
        ('R_A_4_4_-----q------q---', {'A_q_8', 'A_q_7', 'A_q_9', 'A_q_11', 'A_q_14', 'A_q_15', 'A_q_13', 'A_q_4', 'A_q_1', 'A_q_0', 'A_q_6', 'A_q_2', 'A_q_3', 'A_q_10'})
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
    assert puzzle0.toString() == 'R_A_4_4_----------------'


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
    helper(pid, 'R_A_4_4_q---q---q---q---', "4", 3)
