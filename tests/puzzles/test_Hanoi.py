import pytest
import json
import tempfile

from puzzlesolver.puzzles import Hanoi
from puzzlesolver.solvers import GeneralSolver, sqlitesolver
from puzzlesolver.util import *
from puzzlesolver.server import app

def testBaseRemoteness():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        assert solver.getValue(puzzle) == PuzzleValue.SOLVABLE
        assert solver.getRemoteness(puzzle) == 2**i - 1

# Server methods
def testSerialization():
    for i in range(5):
        puzzle = Hanoi(size=i)
        solver = GeneralSolver(puzzle=puzzle)
        solver.solve()
        new_puzzle = Hanoi.deserialize(puzzle.serialize())
        assert hash(puzzle) == hash(new_puzzle)

def testValidation():
    invalid_puzzle = "1_2_3--"
    valid_puzzle = "3_2_1--"
    blank_puzzle = ""
    weird_input = "123__"
    pytest.raises(PuzzleException, Hanoi.validate, blank_puzzle, "3")
    pytest.raises(PuzzleException, Hanoi.validate, weird_input, "3")
    pytest.raises(PuzzleException, Hanoi.validate, invalid_puzzle, "3")
    pytest.raises(PuzzleException, Hanoi.validate, valid_puzzle, "4")
    Hanoi.validate(valid_puzzle, "3")

def test_server_puzzle():
    client = app.test_client()

    sqlitesolver.PATH = tempfile.mkdtemp()

    rv = client.get('/puzzles/hanoi/')
    d = json.loads(rv.data)

    assert d['response']['variants'] == list(Hanoi.variants.keys())

    def helper(code, variantid, remoteness):
        rv = client.get('/puzzles/hanoi/{}/{}/'.format(variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    helper('1--', 1, 1)
    helper('-1-', 1, 1)    
    helper('--1', 1, 0)

    helper('2_1-3-', 3, 4)