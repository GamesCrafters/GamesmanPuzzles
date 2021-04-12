from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleValue

import sys
sys.path.append("../..")

import server
import pytest

# Helper function from server
def generateMovePositions(puzzle, movetype="legal"):
    """Generate an iterable of puzzles with all moves fitting movetype
    executed.

    Inputs:
        - movetype: The type of move to generate the puzzles
    
    Outputs:
        - Iterable of puzzles 
    """
    puzzles = []
    for move in puzzle.generateMoves(movetype=movetype):
        puzzles.append((move, puzzle.doMove(move)))
    return puzzles

def test_correct_path(database_dir):
    for pid in PuzzleManager.getPuzzleIds():
        p_cls = PuzzleManager.getPuzzleClass(pid)
        for variant in p_cls.test_variants:
            s_cls = PuzzleManager.getSolverClass(pid, test=True)
            solver = s_cls(p_cls.generateStartPosition(variant), dir_path=database_dir)
            puzzle = p_cls.generateStartPosition(variant)

            while puzzle.primitive() != PuzzleValue.SOLVABLE:
                assert solver.getValue(puzzle) == PuzzleValue.SOLVABLE, "{} not SOLVABLE".format(puzzle.toString(mode="minimal"))
                positions = generateMovePositions(puzzle)
                prev_remote = solver.getRemoteness(puzzle)
                b = False
                for pos in positions:
                    next_remote = solver.getRemoteness(pos[1])
                    if next_remote != PuzzleValue.UNSOLVABLE and next_remote < prev_remote:
                        puzzle = pos[1]
                        b = True
                if not b: raise AssertionError("Puzzle {} has {} has no moves to reach solution".format(puzzle.__class__.name, puzzle.toString(mode="minimal")))