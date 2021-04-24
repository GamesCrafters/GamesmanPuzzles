
import pytest
import json

from puzzlesolver.puzzles import NQueens, PuzzleManager
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue, PuzzleException


# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    puzzle0 = NQueens.fromString('qq-q----q-------')
    puzzle1 = NQueens.fromString('qq-q----q-------')
    puzzle2 = NQueens.fromString('--------q----qqq')

    # Checks if two exact same puzzles have the same hash
    assert hash(puzzle0) == hash(puzzle1)

    # Checks is two different puzzles have different hash
    assert hash(puzzle0) != hash(puzzle2)


def testSerialization():
    """Tests if serialization and deserialization works both ways."""
    codes = ['qq-q----q-------', 'qqqq------------', '--------q----qqq', '---q---q---q---q', '----qq----qq----']

    for code in codes:
        puzzle = NQueens.fromString(code)
        assert puzzle.toString() == code


def testPrimitive():
    """Tests if the start state and end state outputted the right primitives."""

    # Expected primitive of start state should be UNDECIDED
    puzzle = NQueens.fromString('qqqq------------')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

    # Expected primitive of end state should be SOLVABLE
    puzzle = NQueens.fromString('--q-q------q-q--')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE


def testMoves():
    """Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves."""

    # Tests if state after move matches serialization
    tests = [
        ('qqqq------------', {('03', '22'), ('01', '31'), ('03', '31'), ('02', '22'), ('00', '32'), ('02', '31'), ('00', '23'), ('00', '13'), ('00', '30'), ('00', '10'), ('00', '11'), ('01', '32'), ('00', '33'), ('01', '23'), ('00', '20'), ('03', '32'), ('01', '30'), ('01', '10'), ('01', '13'), ('00', '21'), ('03', '23'), ('02', '32'), ('01', '11'), ('00', '12'), ('03', '13'), ('01', '33'), ('03', '30'), ('03', '10'), ('02', '23'), ('03', '11'), ('01', '20'), ('03', '33'), ('00', '22'), ('02', '10'), ('02', '13'), ('02', '30'), ('03', '20'), ('01', '12'), ('01', '21'), ('02', '11'), ('00', '31'), ('02', '33'), ('03', '21'), ('01', '22'), ('03', '12'), ('02', '20'), ('02', '12'), ('02', '21')}),
        ('----qqqq--------', {('11', '03'), ('11', '22'), ('12', '03'), ('10', '23'), ('12', '22'), ('13', '31'), ('13', '32'), ('10', '01'), ('12', '02'), ('13', '00'), ('12', '21'), ('10', '03'), ('10', '22'), ('11', '02'), ('13', '33'), ('11', '21'), ('12', '20'), ('11', '20'), ('10', '02'), ('11', '30'), ('12', '30'), ('10', '21'), ('13', '23'), ('10', '20'), ('13', '01'), ('10', '30'), ('13', '22'), ('11', '31'), ('12', '31'), ('12', '32'), ('13', '03'), ('11', '32'), ('11', '00'), ('12', '00'), ('11', '33'), ('13', '02'), ('10', '31'), ('12', '33'), ('13', '21'), ('10', '32'), ('13', '20'), ('10', '00'), ('10', '33'), ('13', '30'), ('11', '23'), ('12', '23'), ('11', '01'), ('12', '01')}),
        ('-----q------qqq-', {('30', '00'), ('31', '12'), ('11', '12'), ('31', '03'), ('11', '03'), ('30', '33'), ('11', '10'), ('32', '02'), ('32', '13'), ('31', '21'), ('32', '22'), ('11', '21'), ('31', '20'), ('11', '20'), ('32', '23'), ('30', '02'), ('30', '22'), ('31', '01'), ('30', '13'), ('11', '01'), ('31', '00'), ('11', '00'), ('30', '23'), ('32', '10'), ('31', '33'), ('11', '33'), ('30', '10'), ('32', '12'), ('32', '03'), ('11', '02'), ('11', '22'), ('31', '02'), ('31', '13'), ('11', '13'), ('32', '21'), ('31', '22'), ('32', '20'), ('31', '23'), ('30', '12'), ('11', '23'), ('30', '03'), ('32', '01'), ('30', '21'), ('30', '20'), ('32', '00'), ('31', '10'), ('30', '01'), ('32', '33')})
    ]

    for test in tests:
        puzzle = NQueens.fromString(test[0])
        moves = puzzle.generateMoves()
        print(moves)
        assert moves == test[1]
        for move in moves:
            puzzle.doMove(move)


def testPositions():
    """Tests the default start state matches the expected serializations."""

    puzzle0 = NQueens.generateStartPosition('4')
    assert puzzle0.toString() == 'qqqq------------'


def testValidation():

    """4 invalid serializations"""
    tests = [
        ("", "4"),
        ("qqqqq-------------------", "5"),
        ("qqqqq--------------------", "4"),
        ("qqqq-------------", "4")
    ]
    for test in tests:
        pytest.raises(PuzzleException, PuzzleManager.validate, NQueens.id, test[1], test[0])


def testSolver():
    """Tests the solver functionality of the Puzzle"""

    puzzle = NQueens()
    solver = GeneralSolver(puzzle)
    solver.solve()

    assert solver.getRemoteness(NQueens.fromString('--q--q----q--q--')) == 2


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
    helper(pid, '--q-q------q-q--', "4", 0)
    helper(pid, '--q-q-----q--q--', "4", 1)
    helper(pid, '--q--q----q--q--', "4", 2)
    helper(pid, 'qq-qq-----------', "4", 3)
