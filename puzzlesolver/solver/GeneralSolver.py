from .Solver import Solver
from ..util import *

class GeneralSolver(Solver):

    def __init__(self, *args, **kwargs):
        self.values = {}
        self.remoteness = {}
    
    def getRemoteness(self, puzzle):
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return GameValue.LOSS

    def solve(self, puzzle):
        if hash(puzzle) in self.values: self.values[hash(puzzle)]
        
        def winHelper(self, puzzle):
            for move in puzzle.generateMoves():
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in self.values:
                    self.values[hash(nextPuzzle)] = GameValue.WIN
                    winHelper(self, nextPuzzle)

        def remoteHelper(self, puzzle):
            not_visited = []
            for move in puzzle.generateMoves():
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in self.remoteness: 
                    not_visited.append(move) 
                    self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
            for move in not_visited:
                nextPuzzle = puzzle.doMove(move)
                remoteHelper(self, nextPuzzle)

        ends = puzzle.winStates()
        for end in ends: 
            self.values[hash(end)] = GameValue.WIN
            self.remoteness[hash(end)] = 0
            winHelper(self, end)
            remoteHelper(self, end)
        if hash(puzzle) not in self.values: self.values[hash(puzzle)] = GameValue.LOSS
        return self.values[hash(puzzle)]