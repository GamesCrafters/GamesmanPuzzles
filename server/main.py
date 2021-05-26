from . import app, puzzle_solved_variants
from puzzlesolver.puzzles import PuzzleManager

import os

from threading import Thread

app.config["DEBUG"] = False
app.config["TESTING"] = False
app.config['DATABASE_DIR'] = 'databases'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Start server
def server_start(app):
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

            if os.path.exists(solver.path): 
                puzzle_solved_variants[puzzle_id][variant] = solver

# # Initalizes the data
# def init_data():
#     for p_cls in PuzzleManager.getPuzzleClasses():        
#         if app.config["TESTING"]:
#             variants = p_cls.test_variants
#         else:
#             variants = p_cls.variants
#         for variant in variants:
#             s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)
#             puzzle = p_cls.generateStartPosition(variant)
#             solver = s_cls(puzzle, dir_path=app.config['DATABASE_DIR'])
#             solver.solve(verbose=True)

if __name__ == "__main__":
    host, port = '127.0.0.1', 9001
    if 'GMP_HOST' in os.environ:
        host = os.environ['GMP_HOST']
    if 'GMP_PORT' in os.environ:
        port = os.environ['GMP_PORT']
    app.run(host=host, port=port)    