import flask
from flask import abort
from flask_cors import CORS
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleException, PuzzleValue, StringMode
from werkzeug.exceptions import InternalServerError
from . import puzzle_solved_variants

app = flask.Flask("PuzzleServer")
app.config['DATABASE_DIR'] = 'databases'
app.json_provider_class.compact = False

CORS(app)

# Helper functions

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

# Routes
@app.route('/<puzzle_id>/<variant_id>/start/', methods=['GET'])
def get_start_position(puzzle_id, variant_id):
    validate(puzzle_id, variant_id)
    puzzle = None
    puzzlecls = PuzzleManager.getPuzzleClass(puzzle_id)
    if puzzlecls.startRandomized:
        solved_variants = puzzle_solved_variants[puzzle_id]
        if variant_id not in solved_variants:
            return puzzlecls.generateStartPosition(variant_id)
        s = solved_variants[variant_id]
        hash_val = s.getRandomSolvableHash()
        puzzle = puzzlecls.fromHash(variant_id, hash_val)
    else:
        puzzle = puzzlecls.generateStartPosition(variant_id)

    return {
        'position': puzzle.toString(mode=StringMode.HUMAN_READABLE),
        'autoguiPosition': puzzle.toString(mode=StringMode.AUTOGUI)
    }

@app.route('/<puzzle_id>/<variant_id>/positions/<position>/', methods=['GET'])
def puzzle_position(puzzle_id, variant_id, position):
    validate(puzzle_id, variant_id, position)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).fromString(variant_id, position)
    s = puzzle_solved_variants[puzzle_id][variant_id]
    
    value = s.getValue(puzzle)
    response = {'position': position, 'autoguiPosition': puzzle.toString(mode=StringMode.AUTOGUI), 'positionValue': value}
    if value == PuzzleValue.SOLVABLE:
        response['remoteness'] = s.getRemoteness(puzzle)

    move_objs = []
    for move in puzzle.generateMoves(movetype='legal'):
        child_position = puzzle.doMove(move)
        child_position_value = s.getValue(child_position)
        move_obj = {
            "position": child_position.toString(mode=StringMode.HUMAN_READABLE),
            "autoguiPosition": child_position.toString(mode=StringMode.AUTOGUI),
            "positionValue": child_position_value,
            "move": puzzle.moveString(move, mode=StringMode.HUMAN_READABLE),
            "autoguiMove": puzzle.moveString(move, mode=StringMode.AUTOGUI)
        }
        if child_position_value == PuzzleValue.SOLVABLE:
            move_obj['remoteness'] = s.getRemoteness(child_position)
        move_objs.append(move_obj)
        
    response["moves"] = move_objs
    return response

# Handling Exceptions
@app.errorhandler(InternalServerError)
def handle_500(e):
    return {'error': "Server error"}

@app.errorhandler(404)
def handle_404(e):
    return {'error': str(e)}