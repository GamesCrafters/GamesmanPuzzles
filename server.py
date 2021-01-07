import flask
from flask import request, jsonify, abort
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleException

import os

from werkzeug.exceptions import InternalServerError

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config["TESTING"] = False
app.config['DATABASE_DIR'] = 'databases'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Test your server puzzle
def test_puzzle(puzzle):
    """Helper function to test any puzzle. Sets the PuzzleManager to only hold one Puzzle for testing"""
    from puzzlesolver.puzzles import PuzzleManagerClass
    global PuzzleManager
    puzzleList = {puzzle.puzzleid: puzzle}
    PuzzleManager = PuzzleManagerClass(puzzleList)
    init_data()
    app.run()

# Initalizes the data
# TODO: Check if data already exists in disk before solving
def init_data():
    for p_cls in PuzzleManager.getPuzzleClasses():
        if app.config["TESTING"]:
            variants = p_cls.test_variants
        else:
            variants = p_cls.variants
        for variant in variants:
            s_cls = PuzzleManager.getSolverClass(p_cls.puzzleid, variant)
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=app.config['DATABASE_DIR'])
            solver.solve(verbose=True)

# Helper functions
def validate(puzzleid=None, variantid=None, position=None):
    if puzzleid == None:
        raise ValueError("Nothing to validate")            
    if not PuzzleManager.hasPuzzleId(puzzleid): 
        abort(404, description="PuzzleId not found") 
    if variantid != None:
        variants = PuzzleManager.getPuzzleClass(puzzleid).variants
        if variantid not in variants: 
            abort(404, description="VariantId not found")
    if position != None:
        try:
            PuzzleManager.validate(puzzleid, variantid, position)        
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
        "puzzles": list(PuzzleManager.getPuzzleIds())
    }
    return format_response(response)

@app.route('/<puzzle_id>/', methods=['GET'])
def puzzle(puzzle_id):
    validate(puzzle_id)
    puzzlecls = PuzzleManager.getPuzzleClass(puzzle_id)
    response = {
        "puzzle_id": puzzle_id,
        "puzzle_name": puzzlecls.name,
        "author": puzzlecls.author,
        "description": puzzlecls.description,
        "date_created": puzzlecls.date_created,
        "variants": list(puzzlecls.variants)
    }
    return format_response(response)

@app.route('/<puzzle_id>/<variant_id>/', methods=['GET'])
def puzzle_variant(puzzle_id, variant_id):
    validate(puzzle_id, variant_id)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).generateStartPosition(variant_id)
    response = {
        "starting_pos": puzzle.toString()
    }
    return format_response(response)

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
    
@app.route('/<puzzle_id>/<variant_id>/<position>/', methods=['GET'])
def puzzle_position(puzzle_id, variant_id, position):
    validate(puzzle_id, variant_id, position)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).fromString(position)
    solver_cls = PuzzleManager.getSolverClass(puzzle_id, variant_id, app.config['TESTING'])
    s = solver_cls(puzzle, dir_path=app.config['DATABASE_DIR'])
    moves = generateMovePositions(puzzle)
    response = {
        "position": puzzle.toString(),
        "remoteness": s.getRemoteness(puzzle),
        "value": s.getValue(puzzle),
        "moves": {str(move[0]) : {
            "position": move[1].toString(),
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
