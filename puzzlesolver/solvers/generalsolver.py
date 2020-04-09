from .solver import Solver
from ..util import *
import queue as q

class GeneralSolver(Solver):

    def __init__(self, puzzle, *args, **kwarg):
        self.remoteness = {}
        self.puzzle = puzzle
    
    def getRemoteness(self, puzzle, **kwargs):
        """Returns remoteness of puzzle. Automatically solves if memory isn't set"""
        if not self.remoteness: print("Warning: No memory found. Please make sure that `solve` was called.")
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return PuzzleValue.UNSOLVABLE

    def solve(self, *args, **kwargs):
        """Traverse the entire puzzle tree and classifiers all the 
        positions with values and remoteness
        - If position already exists in memory, returns its value
        """        
        # BFS for remoteness classification
        def helper(self, puzzles):
            queue = q.Queue()
            for puzzle in puzzles: queue.put(puzzle)
            while not queue.empty():
                puzzle = queue.get()
                for move in puzzle.generateMoves('undo'):
                    nextPuzzle = puzzle.doMove(move)
                    if hash(nextPuzzle) not in self.remoteness:
                        remoteness = self.remoteness[hash(puzzle)]
                        self.remoteness[hash(nextPuzzle)] = remoteness + 1
                        queue.put(nextPuzzle)
                        
        ends = self.puzzle.generateSolutions()
        for end in ends: 
            self.remoteness[hash(end)] = 0
        helper(self, ends)