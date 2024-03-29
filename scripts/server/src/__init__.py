puzzle_solved_variants = {}

from .routes import app
from puzzlesolver.puzzles import PuzzleManager

import os

# Test your server puzzle
def test_puzzle(puzzle):
    """Helper function to test any puzzle. Sets the PuzzleManager to only hold one Puzzle for testing"""
    from puzzlesolver.puzzles import PuzzleManagerClass
    global PuzzleManager
    puzzleList = {puzzle.id: puzzle}
    PuzzleManager = PuzzleManagerClass(puzzleList)
    app.run()

with app.app_context():
    # Check which Puzzles have been solved or not solved
    for p_cls in PuzzleManager.getPuzzleClasses():
        if p_cls.id not in puzzle_solved_variants:
            puzzle_solved_variants[p_cls.id] = {}

        variants = p_cls.variants

        for variant in variants:
            p_cls = PuzzleManager.getPuzzleClass(p_cls.id)
            s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)

            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=app.config['DATABASE_DIR'])
            if os.path.exists(solver.path) or solver.path == "closed_form": 
                puzzle_solved_variants[p_cls.id][variant] = solver
