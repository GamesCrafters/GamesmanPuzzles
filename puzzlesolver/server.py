import flask
from flask import request, jsonify, abort
from .puzzles import puzzleList
from .util import PuzzleException

import os

from werkzeug.exceptions import InternalServerError

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config["TESTING"] = False
app.config['DATABASE_DIR'] = 'databases'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Test your server puzzle
def test_puzzle(puzzle):
    global puzzleList
    puzzleList = {puzzle.puzzleid: puzzle}
    init_data()
    app.run()

# Initalizes the data
# TODO: Check if data already exists in disk before solving
def init_data():
    for p_cls in puzzleList.values():
        if app.config["TESTING"] and hasattr(p_cls, 'test_variants'): 
            variants = p_cls.test_variants
        else:
            variants = p_cls.variants
        for variant in variants:
            s_cls = variants[variant]
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=app.config['DATABASE_DIR'])
            solver.solve(verbose=True)

# Helper functions
def validate(puzzle_name=None, variant_id=None, position=None):
    if puzzle_name == None:
        raise ValueError("Nothing to validate")            
    if puzzle_name not in puzzleList: abort(404, description="PuzzleId not found") 
    if variant_id != None:
        variants = puzzleList[puzzle_name].variants
        if variant_id not in variants: abort(404, description="VariantId not found")
    if position != None:
        try:        
            puzzleList[puzzle_name].validate(position, variant_id)
        except PuzzleException as e:
            abort(404, description=str(e))

def format_response(response, status="available"):
    response = {
        "response": response,
        "status": status
    }
    return jsonify(response)

# Routes
@app.route('/', methods=['GET'])
def puzzles():
    response = {
        "puzzles": list(puzzleList.keys())
    }
    return format_response(response)

@app.route('/<puzzle_id>/', methods=['GET'])
def puzzle(puzzle_id):
    validate(puzzle_id)
    puzzle = puzzleList[puzzle_id]
    response = {
        "puzzle_id": puzzle_id,
        "puzzle_name": puzzle.puzzle_name,
        "author": puzzle.author,
        "description": puzzle.description,
        "date_created": puzzle.date_created,
        "variants": list(puzzle.variants.keys())
    }
    return format_response(response)

@app.route('/<puzzle_id>/<variant_id>/', methods=['GET'])
def puzzle_variant(puzzle_id, variant_id):
    validate(puzzle_id, variant_id)
    p = puzzleList[puzzle_id].generateStartPosition(variant_id)
    response = {
        "starting_pos": p.serialize()
    }
    return format_response(response)

@app.route('/<puzzle_id>/<variant_id>/<position>/', methods=['GET'])
def puzzle_position(puzzle_id, variant_id, position):
    validate(puzzle_id, variant_id, position)
    p = puzzleList[puzzle_id].deserialize(position)
    solver_cls = puzzleList[puzzle_id].variants[variant_id]
    s = solver_cls(p, dir_path=app.config['DATABASE_DIR'])
    moves = p.generateMovePositions()
    response = {
        "position": p.serialize(),
        "remoteness": s.getRemoteness(p),
        "value": s.getValue(p),
        "moves": {str(move[0]) : {
            "position": move[1].serialize(),
            "remoteness": s.getRemoteness(move[1]),
            "value": s.getValue(move[1])
        } for move in moves}
    }
    return format_response(response)

# Handling Exceptions
@app.errorhandler(InternalServerError)
def handle_500(e):
    return format_response("Server error", "error")

@app.errorhandler(404)
def handle_404(e):
    return format_response(str(e), "error")

if __name__ == "__main__":
    init_data()
    host, port = '127.0.0.1', 9001
    if 'GMP_HOST' in os.environ:
        host = os.environ['GMP_HOST']
    if 'GMP_PORT' in os.environ:
        port = os.environ['GMP_PORT']
    app.run(host=host, port=port)
