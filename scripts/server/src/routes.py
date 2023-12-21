import flask
from flask import jsonify, abort
from flask_cors import CORS
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleException, PuzzleValue
from puzzlesolver.puzzles.image_autogui_data import *
from puzzlesolver.puzzles.AutoGUI_Status import get_gui_status
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
    if os.path.exists(solver.path) or solver.path == "closed_form":
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

def getPuzzle(puzzle_id, variant_id, randomize):
    puzzlecls = PuzzleManager.getPuzzleClass(puzzle_id)
    if randomize:
        solved_variants = puzzle_solved_variants[puzzle_id]
        if variant_id not in solved_variants:
            return puzzlecls.generateStartPosition(variant_id)
        s = solved_variants[variant_id]
        hash_val = s.getRandomSolvableHash()
        return puzzlecls.fromHash(variant_id, hash_val)
    else:
        return puzzlecls.generateStartPosition(variant_id)

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
            "description": puzzlecls.variants_desc[i],
            "startPosition": getPuzzle(puzzle_id, puzzlecls.variants[i], puzzlecls.startRandomized).toString(),
            "status": check_available(puzzle_id, puzzlecls.variants[i]),
            "variantId": puzzlecls.variants[i],
            'imageAutoGUIData': get_image_autogui_data(puzzle_id, puzzlecls.variants[i]),
            'gui_status': get_gui_status(puzzle_id, puzzlecls.variants[i])
        } for i in range(len(puzzlecls.variants))]
    }
    return format_response(response)

@app.route('/<puzzle_id>/<variant_id>/', methods=['GET'])
@app.route('/<puzzle_id>/variants/<variant_id>/', methods=['GET'])
def puzzle_variant(puzzle_id, variant_id):
    validate(puzzle_id, variant_id)
    puzzlecls = PuzzleManager.getPuzzleClass(puzzle_id)
    puzzle = getPuzzle(puzzle_id, variant_id, puzzlecls.startRandomized)
    
    description = variant_id
    if variant_id in puzzlecls.variants and len(puzzlecls.variants_desc) >= len(puzzlecls.variants):
        description = puzzlecls.variants_desc[puzzlecls.variants.index(variant_id)]
    response = {
        "description": description,
        "startPosition": puzzle.toString(mode="minimal"),
        "status": check_available(puzzle_id, variant_id),
        "variantId": variant_id,
        'imageAutoGUIData': get_image_autogui_data(puzzle_id, variant_id)
    }
    return format_response(response)

@app.route('/<puzzle_id>/<variant_id>/randpos/', methods=['GET'])
@app.route('/<puzzle_id>/variants/<variant_id>/randpos/', methods=['GET'])
def puzzle_randpos(puzzle_id, variant_id):
    validate(puzzle_id, variant_id)
    puzzle = getPuzzle(puzzle_id, variant_id, True)
    response = {
        "position": puzzle.toString(mode="minimal")
    }
    return format_response(response)

def generateMoveData(puzzle, movetype="legal"):
    """Generate an iterable of tuples containing resulting
    puzzles and move string representations based on input movetype.

    Inputs:
        - movetype: The type of move to generate the puzzles
    
    Outputs:
        - Iterable of tuples containing puzzle resulting from move,
        UWAPI representation of the move, and human-readable string
        representation of the move. 
    """
    puzzles = []
    for move in puzzle.generateMoves(movetype=movetype):
        puzzles.append((puzzle.doMove(move), puzzle.moveString(move, 'uwapi'), 
                        puzzle.moveString(move, 'humanreadable')))
    return puzzles

@app.route('/<puzzle_id>/<variant_id>/<position>/', methods=['GET'])
@app.route('/<puzzle_id>/variants/<variant_id>/positions/<position>/', methods=['GET'])
def puzzle_position(puzzle_id, variant_id, position):
    validate(puzzle_id, variant_id, position)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).fromString(position)
    s = puzzle_solved_variants[puzzle_id][variant_id]
    moves = generateMoveData(puzzle)
    
    this_remoteness = s.getRemoteness(puzzle)

    response = {
        "position": puzzle.toString(mode="minimal"),
        "remoteness": this_remoteness 
            if this_remoteness != PuzzleValue.MAX_REMOTENESS
            else -200, # indicates infinite remoteness,
        "positionValue": s.getValue(puzzle),
    }
    move_attr = []
    for move in moves:
        next_remoteness = s.getRemoteness(move[0])
        move_attr.append(
            {
                "position": move[0].toString(mode="minimal"),
                "positionValue": s.getValue(move[0]),
                "move": move[1],
                "moveName": move[2],
                "moveValue": PuzzleValue.UNSOLVABLE
                    if this_remoteness == PuzzleValue.MAX_REMOTENESS
                    else PuzzleValue.SOLVABLE
                    if this_remoteness > next_remoteness
                    else PuzzleValue.NOPROGRESS
                    if this_remoteness == next_remoteness
                    else PuzzleValue.UNSOLVABLE,
                "deltaRemoteness": this_remoteness - next_remoteness,
                "remoteness": next_remoteness
                    if next_remoteness != PuzzleValue.MAX_REMOTENESS
                    else -200, # indicates infinite remoteness,
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
