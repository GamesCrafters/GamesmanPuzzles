#!usr/bin/env python3
from flask import Flask, jsonify

from puzzlesolver import puzzleList    

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["DEBUG"] = True

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
                'startPosition': puzzleList[id]['puzzle']().encode()
            }
        for id in puzzleList])
    except: format_response_err()

@app.route('/puzzles/<puzzle_id>/positions/<position>', methods=['GET'])
def handle_position(puzzle_id, position):
    try:
        puzzle = puzzleList[puzzle_id]['puzzle'](id=position)
        solver = puzzleList[puzzle_id]['solver'](puzzle=puzzle, path="./database")
        return format_response_ok({
            'position': position,
            'positionValue': solver.solve(puzzle),
            'remoteness': solver.getRemoteness(puzzle),
            'moves': [
                {
                    "move": move,
                    "position": puzzle.doMove(move).encode(),
                    "positionValue": solver.solve(puzzle.doMove(move)),
                    "remoteness": solver.getRemoteness(puzzle.doMove(move))
                } for move in puzzle.generateLegalMoves()
            ]
        })    
    except AssertionError:
        return format_response_err("Invalid position ID")
    except:
        return format_response_err()

"""
@app.route('/puzzles/<puzzle_id>', methods=['GET'])
def handle_puzzle(puzzle_id):
    if puzzle_id != 'hanoi': return format_response_err('Game not found')
    return format_response_ok({
        'puzzleId': puzzle_id,
        'name': 'Hanoi',
        'variants': [
            {
                'variantId': 'regular',
                'description': '',
                'status': 'ok',
            }
        ]
    })
"""

if __name__ == '__main__':
    app.run(port=9001)