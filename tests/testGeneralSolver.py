import pytest

from puzzlesolver.puzzles import GraphPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def testSimple():
    forward = GraphPuzzle(0)
    bidirectional = GraphPuzzle(1)
    backward = GraphPuzzle(2)
    sol = GraphPuzzle(3, value=PuzzleValue.SOLVABLE)

    sol.setMove(forward, movetype="for")
    sol.setMove(bidirectional, movetype="bi")
    sol.setMove(backward, movetype="back")

    solver = GeneralSolver()
    solver.solve(sol)

    assert solver.getRemoteness(backward) == 1
    assert solver.getRemoteness(sol) == 0
    assert solver.getRemoteness(bidirectional) == 1
    assert solver.getRemoteness(forward) == PuzzleValue.UNSOLVABLE