import pytest

from puzzlesolver.puzzles.graphpuzzle import GraphPuzzle
from puzzlesolver.util import *

def testPaths():
    puzzle1 = GraphPuzzle(0)
    puzzle2 = GraphPuzzle(1)
    puzzle3 = GraphPuzzle(2)
    puzzle4 = GraphPuzzle(3)
    
    puzzle1.setMove(puzzle2)
    puzzle1.setMove(puzzle3, "bi")
    puzzle1.setMove(puzzle4, "back")

    assert puzzle1.doMove(1) == puzzle2
    assert puzzle1.doMove(2) == puzzle3
    assert puzzle1.doMove(3) == puzzle4
"""
def testForwardPath():
    lastPuzzle = GraphPuzzle(0) 
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
"""