#!usr/bin/env python3
from flask import Flask, jsonify

from puzzlesolver.solver import PickleSolverWrapper
from puzzlesolver.puzzle import Hanoi

app = Flask(__name__)
app.config["DEBUG"] = True

puzzle = Hanoi()
solver = PickleSolverWrapper(puzzle=puzzle, path="./database/")

@app.route('/get/<name>', methods=['GET'])
def get(name):
    return solver.solve(puzzle)