import flask
from flask import request, jsonify, abort
from flask_cors import CORS
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleException, PuzzleValue
from puzzlesolver.puzzles.AutoGUI_Status import get_gui_status

import os

from threading import Thread
from werkzeug.exceptions import InternalServerError

from . import puzzle_solved_variants

app = flask.Flask("PuzzleServer")
app.config["DEBUG"] = False
app.config["TESTING"] = False
app.config['DATABASE_DIR'] = 'databases'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app)

def check_available(puzzle_id, variant=None):

    if puzzle_id not in puzzle_solved_variants:
        puzzle_solved_variants[puzzle_id] = {}
        if variant is None: return "unknown"
    elif len(puzzle_solved_variants[puzzle_id]) == 0:
        return "unavailable"
    elif variant is None or variant in puzzle_solved_variants[puzzle_id]:
        return "available"

    p_cls = PuzzleManager.getPuzzleClass(puzzle_id)
    s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)

    puzzle = p_cls.generateStartPosition(variant)
    solver = s_cls(puzzle, dir_path=app.config['DATABASE_DIR'])

    import os
    if os.path.exists(solver.path): 
        puzzle_solved_variants[puzzle_id][variant] = solver
        return "available"
    return "not available"

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
        if check_available(puzzleid, variantid) != "available":
            abort(404, description="Puzzle is unavailable")
    if position != None:
        try:
            PuzzleManager.validate(puzzleid, variantid, position)        
        except PuzzleException as e:
            abort(404, description=str(e))

def format_response(response, status="ok"):
    response = {
        "response": response,
        "status": status
    }
    return jsonify(response)

# Routes
@app.route('/', methods=['GET'])
def puzzles():
    response = [
        {
            "gameId": puzzle_id,
            "name"  : PuzzleManager.getPuzzleClass(puzzle_id).name,
            "status": check_available(puzzle_id),
            "gui_status": get_gui_status(puzzle_id)
        }
        for puzzle_id in PuzzleManager.getPuzzleIds()
    ]
    response.sort(key=lambda p: p["name"])
    return format_response(response)

@app.route('/<puzzle_id>/', methods=['GET'])
@app.route('/<puzzle_id>/variants/', methods=['GET'])
def puzzle(puzzle_id):
    validate(puzzle_id)
    puzzlecls = PuzzleManager.getPuzzleClass(puzzle_id)
    response = {
        "gameId":           puzzle_id,
        "name":             puzzlecls.name,
        "author":           puzzlecls.auth,
        "description":      puzzlecls.desc,
        "date_created":     puzzlecls.date,
        "variants":         [{
            "description": variant_id,
            "startPosition": puzzlecls.generateStartPosition(variant_id).toString(),
            "status": check_available(puzzle_id, variant_id),
            "gui_status": get_gui_status(puzzle_id, variant_id),
            "variantId": variant_id
        } for variant_id in puzzlecls.variants]
    }
    return format_response(response)

@app.route('/<puzzle_id>/<variant_id>/', methods=['GET'])
@app.route('/<puzzle_id>/variants/<variant_id>/', methods=['GET'])
def puzzle_variant(puzzle_id, variant_id):
    validate(puzzle_id, variant_id)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).generateStartPosition(variant_id)
    response = {
        "description": variant_id,
        "startPosition": puzzle.toString(mode="minimal"),
        "status": check_available(puzzle_id, variant_id),
        "gui_status": get_gui_status(puzzle_id, variant_id),
        "variantId": variant_id
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
@app.route('/<puzzle_id>/variants/<variant_id>/positions/<position>/', methods=['GET'])
def puzzle_position(puzzle_id, variant_id, position):
    validate(puzzle_id, variant_id, position)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).fromString(position)
    s = puzzle_solved_variants[puzzle_id][variant_id]
    moves = generateMovePositions(puzzle)
    
    this_remoteness = s.getRemoteness(puzzle)

    response = {
        "position": puzzle.toString(mode="minimal"),
        "remoteness": this_remoteness 
        if this_remoteness != PuzzleValue.MAX_REMOTENESS
        else -1,
        "positionValue": s.getValue(puzzle),
    }
    move_attr = []
    for move in moves:
        next_remoteness = s.getRemoteness(move[1])
        move_attr.append(
            {
                "position": move[1].toString(mode="minimal"),
                "positionValue": s.getValue(move[1]),
                "move": str(move[0]),
                "moveValue": PuzzleValue.SOLVABLE
                if this_remoteness > next_remoteness
                else PuzzleValue.UNDECIDED
                if this_remoteness == next_remoteness
                else PuzzleValue.UNSOLVABLE,
                "deltaRemoteness": this_remoteness - next_remoteness,
                "remoteness": next_remoteness
                if next_remoteness != PuzzleValue.MAX_REMOTENESS
                else -1,
            }
        )
        response["moves"] = move_attr

    return format_response(response)

# Handling Exceptions
@app.errorhandler(InternalServerError)
def handle_500(e):
    return format_response("Server error", "error")

@app.errorhandler(404)
def handle_404(e):
    return format_response(str(e), "error")