#!usr/bin/env python3
from flask import Flask, jsonify

from puzzlesolver.solver.PickleSolverWrapper import PickleSolverWrapper
from puzzlesolver.puzzles.Hanoi import Hanoi

app = Flask(__name__)

puzzle = Hanoi()
solver = PickleSolverWrapper(puzzle=puzzle, path="./database/")

@app.route('/get/<name>', methods=['GET'])
def get(name):
    return solver.solve(puzzle)