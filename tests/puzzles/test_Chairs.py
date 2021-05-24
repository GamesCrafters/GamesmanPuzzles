import pytest
import json

from puzzlesolver.puzzles import Chairs, PuzzleManager
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

# Unit testing
def testHash():
    puzzle0 = Chairs.fromString('R_A_1_11_xxxxx-ooooo')
    puzzle1 = Chairs.fromString('R_A_1_11_xxxxx-ooooo')
    puzzle2 = Chairs.fromString('R_A_1_11_ooxxx-oxxoo')
    puzzle3 = Chairs.fromString('R_A_1_11_oo-xxxoxxoo')
    assert hash(puzzle0) == hash(puzzle1)
    #assert hash(puzzle0) == hash(puzzle2)
    assert hash(puzzle0) != hash(puzzle3)

def testSerialization():
    codes = ['R_A_1_11_ooxxx-oxxoo', 'R_A_1_11_-ooxxxoxxoo', 'R_A_1_11_ooooo-xxxxx', 'R_A_1_11_xxxxxooo-oo', 'R_A_1_12_xxx-xxoxoooo']
    for code in codes:
        puzzle = Chairs.fromString(code)
        assert puzzle.toString() == code

def testPrimitive():
    puzzle = Chairs.fromString('R_A_1_11_ooooo-xxxxx')
    assert puzzle.primitive() == PuzzleValue.SOLVABLE
    puzzle = Chairs.fromString('R_A_1_11_xxxxx-ooooo')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED
    puzzle = Chairs.fromString('R_A_1_11_ooooox-xxxx')
    assert puzzle.primitive() == PuzzleValue.UNDECIDED

def testMoves():
    puzzle0 = Chairs.fromString('R_A_1_11_xxxxx-ooooo')
    puzzle1 = puzzle0.doMove("M_4_5")
    assert puzzle1.toString() == 'R_A_1_11_xxxx-xooooo'
    puzzle2 = puzzle1.doMove("M_6_4")
    assert puzzle2.toString() == 'R_A_1_11_xxxxox-oooo'
    puzzle3 = puzzle2.doMove("M_5_6")
    assert puzzle3.toString() == 'R_A_1_11_xxxxo-xoooo'

    with pytest.raises(Exception): puzzle1.doMove("M_11_12")
    with pytest.raises(Exception): puzzle0.doMove("M_2_3")
    with pytest.raises(Exception): puzzle0.doMove("M_8_7")
    with pytest.raises(Exception): puzzle0.doMove("")

    assert len(puzzle0.generateMoves(movetype='for')) == 2
    assert len(puzzle1.generateMoves(movetype='for')) == 2
    assert len(puzzle2.generateMoves(movetype='for')) == 2
    assert len(puzzle3.generateMoves(movetype='for')) == 2

def testPositions():
    puzzle0 = Chairs.generateStartPosition('10')
    assert puzzle0.toString() == 'R_A_1_11_xxxxx-ooooo'
    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1

def testValidation():

    tests = [
        ("", "10"),
        ("R_A_1_11_xxxyx_ooo--oo", "10"),
        ("R_A_1_11_xxxoo-ooooo", "10"),
        ("R_A_1_11_xxxoo-ooooo", "10")
    ]

    for test in tests:
        try:
            PuzzleManager.validate(Chairs.id, test[1], test[0])
        except PuzzleException:
            continue
        raise AssertionError("Str: %s and Variant: %s didn't return PuzzleException" % test)
    PuzzleManager.validate(Chairs.id, "10", "R_A_1_11_oooxx-ooxxx")

def testPuzzleServer(client):
    pid = Chairs.id
    rv = client.get('/{}/'.format(pid))
    d = json.loads(rv.data)

    for variant in d['response']["variants"]:
        assert variant['variantId'] in Chairs.variants

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    helper(pid, 'R_A_1_11_ooooo-xxxxx', '10', 0)
    helper(pid, 'R_A_1_11_xxxxx-ooooo', '10', 35)
    helper(pid, 'R_A_1_11_xxxxxooooo-', '10', -1)
