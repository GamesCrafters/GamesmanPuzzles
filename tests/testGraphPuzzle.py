import pytest

from puzzlesolver.puzzles.graphpuzzle import GraphPuzzle
from puzzlesolver.util import *
from puzzlesolver.util import PuzzleValue as pz

def testMoveGeneral():
    puzzle1 = GraphPuzzle(0)
    puzzle2 = GraphPuzzle(1)
    puzzle3 = GraphPuzzle(2)
    puzzle4 = GraphPuzzle(3)
    
    puzzle1.setMove(puzzle2, "for")
    puzzle1.setMove(puzzle3, "bi")
    puzzle1.setMove(puzzle4, "back")

    forward = puzzle1.generateMoves(movetype='for')
    assert len(forward) == 1
    assert puzzle1.doMove(next(iter(forward))) == puzzle2

    bi = puzzle1.generateMoves(movetype='bi')
    assert len(bi) == 1
    assert puzzle1.doMove(next(iter(bi))) == puzzle3

    back = puzzle1.generateMoves(movetype='back')
    assert len(back) == 1
    assert puzzle1.doMove(next(iter(back))) == puzzle4

    assert len(puzzle1.generateMoves(movetype='legal')) == 2
    assert len(puzzle1.generateMoves(movetype='undo')) == 2

    assert puzzle1.graph == puzzle2.graph
    assert puzzle1.graph == puzzle3.graph
    assert puzzle1.graph == puzzle4.graph

def testInvalid():
    pytest.raises(Exception, GraphPuzzle)
    pytest.raises(ValueError, GraphPuzzle, 0, value=None)

    gp1 = GraphPuzzle(0, value=pz.UNDECIDED)
    gp2 = GraphPuzzle(1, value=pz.SOLVABLE)
    gp3 = GraphPuzzle(1, value=pz.UNDECIDED)
    gp1.setMove(gp2)
    pytest.raises(ValueError, gp1.setMove, gp1)
    pytest.raises(ValueError, gp1.setMove, gp3)

    pytest.raises(ValueError, gp1.doMove, None)
    pytest.raises(ValueError, gp1.doMove, 10)
    pytest.raises(ValueError, gp1.doMove, next(iter(gp2.generateMoves())))

    gp4 = GraphPuzzle(2, value=pz.UNDECIDED)
    gp4.setMove(gp3)

    pytest.raises(ValueError, gp1.setMove, gp4)

"""
def testCase1():
    p1 = GraphPuzzle(1)
    p2 = GraphPuzzle(2)
    p1.setMove(p2)
    p3 = GraphPuzzle(3)
    p3.setMove(p1)
    p3.setMove(p1, movetype='bi')
    assert p1.graph == p2.graph
    assert p1.graph == p3.graph
"""