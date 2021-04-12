from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleValue

# Test if solutions are solved
def test_solution_are_solved():
    string = "{} puzzle with variant {} has a solution {} that is not SOLVABLE."

    for p_cls in PuzzleManager.getPuzzleClasses():
        for variantid in p_cls.variants:
            puzzle = p_cls.generateStartPosition(variantid)
            solutions = puzzle.generateSolutions()
            if solutions is not None:
                for sol in solutions:
                    assert sol.primitive() == PuzzleValue.SOLVABLE, string.format(p_cls.name, variantid, sol.toString(mode="minimal"))

# Add an additional test for undo moves