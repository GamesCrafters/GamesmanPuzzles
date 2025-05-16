import flask
from flask import abort, request
from flask_cors import CORS
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.util import PuzzleException, PuzzleValue, StringMode
from werkzeug.exceptions import InternalServerError
from . import puzzle_solved_variants
import time
import psutil
from datetime import datetime, timezone

app = flask.Flask("PuzzleServer")
app.config['DATABASE_DIR'] = 'databases'
app.json_provider_class.compact = False

start_time = time.time()

CORS(app)

# Helper functions

def check_available(puzzle_id, variant=None):

    if puzzle_id not in puzzle_solved_variants:
        puzzle_solved_variants[puzzle_id] = {}
        if variant is None: 
            return "unknown"
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

def format_time(seconds: float) -> str:
    seconds = int(seconds)
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{days}d {hours}h {minutes}m {secs}s"

# Routes

@app.route('/health')
def get_health():
    uptime_seconds = time.time() - start_time
    uptime = format_time(uptime_seconds)
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    process_count = len(psutil.pids())
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    
    return {
        'status': "ok" if cpu_usage < 90 and memory.percent < 90 else "degraded",
        'http_code': 200,
        'uptime': uptime,
        'cpu_usage': f"{cpu_usage}%", 
        'memory_usage': f"{memory.percent}%",
        'process_count': process_count,
        'timestamp': timestamp,
    }, 200

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

@app.route('/<puzzle_id>/<variant_id>/positions/', methods=['GET'])
def puzzle_position(puzzle_id, variant_id):
    position = request.args.get('p', None)
    if not position:
        abort(404, description="Position not found")
    validate(puzzle_id, variant_id, position)
    puzzle = PuzzleManager.getPuzzleClass(puzzle_id).fromString(variant_id, position)
    s = puzzle_solved_variants[puzzle_id][variant_id]

    # We put this special case for towers of hanoi temporarily because we currently
    # don't have support for SOLVABLE positions with remoteness > 126.
    get_value = (lambda _: PuzzleValue.SOLVABLE) if puzzle_id == 'towersofhanoi' else s.getValue

    value = get_value(puzzle)
    response = {'position': position, 'autoguiPosition': puzzle.toString(mode=StringMode.AUTOGUI), 'positionValue': value}
    if value == PuzzleValue.SOLVABLE:
        response['remoteness'] = s.getRemoteness(puzzle)

    move_objs = []
    for move in puzzle.generateMoves(movetype='legal'):
        child_position = puzzle.doMove(move)
        child_position_value = get_value(child_position)
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