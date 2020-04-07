import flask
from flask import request, jsonify, abort
from .puzzles import puzzleList
from .util import PuzzleException

from werkzeug.exceptions import InternalServerError

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Test your server puzzle
def test_puzzle(puzzle):
    global puzzleList
    puzzleList = {puzzle.puzzleid: puzzle}
    app.run()

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

@app.route('/puzzles/<puzzle_id>/', methods=['GET'])
def puzzle(puzzle_id):
    validate(puzzle_id)
    puzzle = puzzleList[puzzle_id]
    response = {
        "puzzle_id": puzzle_id,
        "puzzle_name": puzzle.puzzle_name,
        "description": puzzle.description,
        "date_created": puzzle.date_created,
        "variants": list(puzzle.variants.keys())
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9001)