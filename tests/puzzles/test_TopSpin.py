import pytest
import json

from puzzlesolver.puzzles import TopSpin, PuzzleManager
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue, PuzzleException

def testHash():
    puzzle0 = TopSpin.deserialize('1_4-2-3-6-5')
    puzzle1 = TopSpin.deserialize('1_4-2-3-6-5')
    puzzle2 = TopSpin.deserialize('2_5-3-6-1-4')
    assert hash(puzzle0) == hash(puzzle1)
    assert hash(puzzle1) != hash(puzzle2)

def testSerialization():
    codes = ['1_4-2-3-6-5','2_5-3-6-1-4', '3_4-5-2-1-6','4_6-3-2-1-5']
    for code in codes:
        puzzle = TopSpin.deserialize(code)
        assert puzzle.serialize() == code

def testPrimitive():
    puzzle0 = TopSpin.deserialize('1_2-3-4-5-6')
    assert puzzle0.primitive() == PuzzleValue.SOLVABLE
    puzzle1 = TopSpin.deserialize('4_2-1-5-6-3')
    assert puzzle1.primitive() == PuzzleValue.UNDECIDED


def testMoves():
    #test rotate
    puzzle0 = TopSpin.deserialize('2_4-1-3-5-6')
    puzzle1 = puzzle0.doMove((3, 'clockwise'))
    assert puzzle1.serialize() == '3_5-6-2-4-1'
    puzzle2 = puzzle1.doMove((1, 'clockwise'))
    assert puzzle2.serialize() == '1_3-5-6-2-4'

    #test flip
    puzzle3 = puzzle0.doMove(('flip'))
    assert puzzle3.serialize() == '4_2-1-3-5-6'

    # Invalid moves raises an Exception
    with pytest.raises(Exception): puzzle1.doMove(('move'))
    with pytest.raises(Exception): puzzle0.doMove((6, 'clockwise'))
    with pytest.raises(Exception): puzzle0.doMove(-1, 'clockwise')

    # Length of generated moves should match expected.
    assert len(puzzle0.generateMoves()) == 6
    assert len(puzzle1.generateMoves()) == 6
    assert len(puzzle2.generateMoves()) == 6
    assert len(puzzle3.generateMoves()) == 6


def testPositions():
    puzzle0 = TopSpin.generateStartPosition('6_2')
    assert len(puzzle0.loop) == 6 and len(puzzle0.track[0]) == 2 and len(puzzle0.track) == 5
    assert max(puzzle0.loop) == 6 and min(puzzle0.loop) == 1

    puzzles = puzzle0.generateSolutions()
    assert len(puzzles) == 1
    assert puzzles[0].serialize() == '1_2-3-4-5-6'

def testValidation():
    tests = [
        ("", "6_2"),
        ("0_1-2-3-4-5", "6_2"),
        ("2_3-1-4-5-20", "6_2"),
        ("4_5-6-1-2-2", "6_2"),
        ("123456----", "6_2")
    ]

    for test in tests:
        pytest.raises(PuzzleException, PuzzleManager.validate, TopSpin.id, test[0], test[1])
    PuzzleManager.validate(TopSpin.id, "6_2", "2_1-5-3-6-4")

def testServerPuzzle(client):
    pid = TopSpin.id
    rv = client.get('/{}/'.format(pid))
    d = json.loads(rv.data)

    for variant in d['response']["variants"]:
        assert variant['variantId'] in TopSpin.variants

    def helper(puzzleid, code, variantid, remoteness):
        rv = client.get('/{}/{}/{}/'.format(puzzleid, variantid, code))
        d = json.loads(rv.data)
        assert d['response']['remoteness'] == remoteness
    
    helper(pid, '1_2-3-4-5-6', '6_2', 0)
    helper(pid, '2_1-3-4-5-6', '6_2', 1)    
    helper(pid, '2_3-4-5-6-1', '6_2', 1)

    helper(pid, '1_2-6-3-5-4', '6_2', 7)