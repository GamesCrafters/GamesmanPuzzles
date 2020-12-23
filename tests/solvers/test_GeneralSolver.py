import pytest

from puzzlesolver.puzzles import GraphPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import PuzzleValue

########################################################################
# Tests
########################################################################

def testSimple(simple):
    simple(GeneralSolver, csp=False)
    simple(GeneralSolver, csp=True)

def testSolutionsError():
    record_sol = GraphPuzzle(0, value=PuzzleValue.SOLVABLE)
    missed_sol = GraphPuzzle(1, value=PuzzleValue.SOLVABLE)
    not_a_solu = GraphPuzzle(2)

    record_sol.setMove(missed_sol, movetype="bi")
    record_sol.setMove(not_a_solu, movetype="bi")

    # Two solutions, but only one is called in generateSolutions
    record_sol.solutions.remove(missed_sol)

    try:
        solver = GeneralSolver(record_sol)
        solver.solve()
    except AssertionError:
        pass

    # generateSolutions also includes a state that is not a solution
    record_sol.solutions.update(set([record_sol, missed_sol, not_a_solu]))

    try:
        solver = GeneralSolver(record_sol)
        solver.solve()
    except AssertionError:
        pass