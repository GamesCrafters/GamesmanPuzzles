#!usr/bin/env python3
from flask import Flask, jsonify, redirect, url_for

from puzzlesolver import puzzleList    

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["DEBUG"] = True

API_PORT=9001

try: 
    from flask_cors import CORS
    CORS(app)
except:
    pass

def format_response_ok(response):
    return {
        'status': 'ok',
        'response': response
    }

def format_response_err(error_message="No message available"):
    return {
        'status': 'error',
        'error': error_message
    }

@app.route('/puzzles', methods=['GET'])
def handle_puzzles():
    try:
        return format_response_ok([
            {
                'gameId': id,
                'name': puzzleList[id]['name'],
            }
        for id in puzzleList])
    except: 
        return format_response_err()

@app.route('/puzzles/<puzzle_id>/variants', methods=['GET'])
def handle_puzzle_variants(puzzle_id):
    try:
        return format_response_ok({
            'puzzleId': puzzle_id,
            'name': 'Hanoi',
            'variants': [
                {
                    'variantId': variant_id,
                    'description': '',
                    'status': 'ok',
                } for variant_id in puzzleList[puzzle_id]['variants']
            ]      
        })
    except:
        return format_response_err()

@app.route('/puzzles/<puzzle_id>/variants/<variant_id>', methods=['GET'])
def handle_puzzle_variant(puzzle_id, variant_id):
    try:
        variant = puzzleList[puzzle_id]['variants'][variant_id]
        return format_response_ok({
            'startPos': variant['puzzle']().encode()
        })
    except AssertionError:
        return format_response_err()

@app.route('/puzzles/<puzzle_id>/variants/<variant_id>/positions/<position>', methods=['GET'])
def handle_position(puzzle_id, variant_id, position):
    try:
        puzzle = puzzleList[puzzle_id]['variants'][str(variant_id)]['puzzle'](position_id=position)
        solver = puzzleList[puzzle_id]['variants'][str(variant_id)]['solver'](puzzle=puzzle, path="./database")
        return format_response_ok({
            'position': position,
            'positionValue': solver.solve(puzzle),
            'remoteness': solver.getRemoteness(puzzle),
            'moves': [
                {
                    "move": str(move),
                    "position": puzzle.doMove(move).encode(),
                    "positionValue": solver.solve(puzzle.doMove(move)),
                    "remoteness": solver.getRemoteness(puzzle.doMove(move))
                } for move in puzzle.generateLegalMoves()
            ]
        })    
    except AssertionError:
        return format_response_err("Invalid position ID")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)