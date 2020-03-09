import pytest

from puzzlesolver.puzzles.graphpuzzle import GraphPuzzle
from puzzlesolver.util import *

@GraphPuzzle.variant_test
def testInit():
    with pytest.raises(ValueError): GraphPuzzle()
    GraphPuzzle(name=1)
    with pytest.raises(ValueError): GraphPuzzle(name=1)
    GraphPuzzle(name=2)

@GraphPuzzle.variant_test
def testVariant():
    v0p1 = GraphPuzzle(name=1, variantid=0)
    GraphPuzzle(name=2, variantid=0)
    with pytest.raises(ValueError): GraphPuzzle(name=2, variantid=0)
    print(GraphPuzzle(name=1, variantid=1))
    with pytest.raises(ValueError): GraphPuzzle(name=2, forwardChildren=[v0p1], variantid=1)
    with pytest.raises(ValueError): GraphPuzzle(name=2, biChildren=[v0p1], variantid=1)

@GraphPuzzle.variant_test
def testForwardPath():
    lastPuzzle = GraphPuzzle(name=0) 
    firstPuzzle = lastPuzzle
    for i in range(1, 3):
        firstPuzzle = GraphPuzzle(name=i, forwardChildren=[firstPuzzle])

    puzzle = firstPuzzle
    for _ in range(1, 3):
        moves = puzzle.generateMoves(movetype='legal')
        assert moves
        assert len(moves) == 1
        puzzle = puzzle.doMove(moves[0])

    assert puzzle == lastPuzzle, '{} is not {}'.format(puzzle, lastPuzzle)
    assert not puzzle.generateMoves(movetype='legal')

@GraphPuzzle.variant_test
def testUndoPath():
    lastPuzzle = GraphPuzzle(name=0) 
    firstPuzzle = lastPuzzle
    for i in range(1, 3):
        firstPuzzle = GraphPuzzle(name=i, forwardChildren=[firstPuzzle])

    puzzle = lastPuzzle
    for _ in range(1, 3):
        moves = puzzle.generateMoves(movetype="undo")
        assert moves
        assert len(moves) == 1
        puzzle = puzzle.doMove(moves[0])

    assert puzzle == firstPuzzle, '{} is not {}'.format(puzzle, lastPuzzle)
    assert not puzzle.generateMoves(movetype="undo")

@GraphPuzzle.variant_test
def testBiPath():
    lastPuzzle = GraphPuzzle(0)
    firstPuzzle = lastPuzzle
    for i in range(1, 2):
        firstPuzzle = GraphPuzzle(i, biChildren=[firstPuzzle])
    
    cur, other = firstPuzzle, lastPuzzle
    assert cur != other
    for _ in range(2):
        moves = cur.generateMoves(movetype="bi")
        assert moves
        assert len(moves) == 1
        temp = cur.doMove(moves[0])
        assert temp != cur
        assert temp == other
        cur, other = temp, cur        