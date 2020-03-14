import flask
from flask import request, jsonify
from puzzlesolver.puzzles import puzzleList

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/puzzles', methods=['GET'])
def puzzles():
    response = {
        "available puzzles": list(puzzleList.keys())
    }
    return jsonify(response)

@app.route('/puzzles/<puzzle_name>', methods=['GET'])
def puzzle(puzzle_name):
    if puzzle_name not in puzzleList: 
        return "Error"
    response = {
        "puzzle name": puzzle_name,
        "variants": list(puzzleList[puzzle_name].variants.keys())
    }
    return jsonify(response)

@app.route('/puzzles/<puzzle_name>/<variant_id>', methods=['GET'])
def puzzle_variant(puzzle_name, variant_id):
    if puzzle_name not in puzzleList:
        return "Error"
    if int(variant_id) not in puzzleList[puzzle_name].variants.keys():
        return "Error"
    p = puzzleList[puzzle_name]()
    response = {
        "puzzle name": puzzle_name,
        "variant_id": int(variant_id),
        "starting_pos": p.serialize()
    }
    return jsonify(response)

@app.route('/puzzles/<puzzle_name>/<variant_id>/<position>', methods=['GET'])
def puzzle_position(puzzle_name, variant_id, position):
    variant_id = int(variant_id)
    if puzzle_name not in puzzleList:
        return "Error"
    if int(variant_id) not in puzzleList[puzzle_name].variants.keys():
        return "Error"
    p = puzzleList[puzzle_name].deserialize(position)
    s = puzzleList[puzzle_name].variants[variant_id](p)
    s.solve()
    response = {
        "puzzle name": puzzle_name,
        "variant_id": int(variant_id),
        "position": p.serialize(),
        "remoteness": s.getRemoteness(p),
        "value": s.getValue(p)
    }
    return jsonify(response)

app.run()