import pytest

from puzzlesolver.puzzles import GraphPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def testSimple(simple):
    simple(GeneralSolver)
    
def testCSP():
    forward = GraphPuzzle(0, csp=True)
    bidirectional = GraphPuzzle(1, csp=True)
    backward = GraphPuzzle(2, csp=True)
    sol = GraphPuzzle(3, value=PuzzleValue.SOLVABLE, csp=True)

    sol.setMove(forward, movetype="for")
    sol.setMove(bidirectional, movetype="bi")
    sol.setMove(backward, movetype="back")

    solver = GeneralSolver(sol)
    solver.solve()

    assert solver.getRemoteness(backward) == 1
    assert solver.getRemoteness(sol) == 0
    assert solver.getRemoteness(bidirectional) == 1
    assert solver.getRemoteness(forward) == PuzzleValue.UNSOLVABLE
    print("CSP test: Successful")
