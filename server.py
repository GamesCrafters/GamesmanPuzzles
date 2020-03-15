import flask
from flask import request, jsonify, abort
from puzzlesolver.puzzles import puzzleList
from puzzlesolver.util import *

from werkzeug.exceptions import *

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
@app.route('/puzzles/', methods=['GET'])
def puzzles():
    response = {
        "puzzles": list(puzzleList.keys())
    }
    return format_response(response)

@app.route('/puzzles/<puzzle_name>/', methods=['GET'])
def puzzle(puzzle_name):
    validate(puzzle_name)
    response = {
        "puzzle name": puzzle_name,
        "variants": list(puzzleList[puzzle_name].variants.keys())
    }
    return format_response(response)

@app.route('/puzzles/<puzzle_name>/<variant_id>/', methods=['GET'])
def puzzle_variant(puzzle_name, variant_id):
    validate(puzzle_name, variant_id)
    p = puzzleList[puzzle_name].generateStartPosition(variant_id)
    response = {
        "starting_pos": p.serialize()
    }
    return format_response(response)

@app.route('/puzzles/<puzzle_name>/<variant_id>/<position>/', methods=['GET'])
def puzzle_position(puzzle_name, variant_id, position):
    validate(puzzle_name, variant_id, position)
    p = puzzleList[puzzle_name].deserialize(position)
    s = puzzleList[puzzle_name].variants[variant_id](p)
    s.solve()
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

app.run()