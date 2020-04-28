from .solver import Solver
from ..util import *
import queue as q
import progressbar

class GeneralSolver(Solver):

    def __init__(self, puzzle, *args, **kwarg):
        self.remoteness = {}
        self.puzzle = puzzle
    
    def getRemoteness(self, puzzle, **kwargs):
        """Returns remoteness of puzzle. Automatically solves if memory isn't set"""
        if not self.remoteness: print("Warning: No memory found. Please make sure that `solve` was called.")
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return PuzzleValue.UNSOLVABLE

    def solve(self, *args, verbose=False, **kwargs):
        """Traverse the entire puzzle tree and classifiers all the 
        positions with values and remoteness
        - If position already exists in memory, returns its value
        """
        if verbose: 
            bar = progressbar.ProgressBar()
            if hasattr(self.puzzle, 'numPositions'): bar.max_value = self.puzzle.numPositions
        solutions, queue = self.puzzle.generateSolutions(), q.Queue()
        for solution in solutions: 
            self.remoteness[hash(solution)] = 0
            queue.put(solution)

        # BFS for remoteness classification                        
        while not queue.empty():
            if verbose: bar.update(len(self.remoteness) + 1)
            puzzle = queue.get()
            for move in puzzle.generateMoves('undo'):
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in self.remoteness:
                    self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                    queue.put(nextPuzzle)
        if verbose: bar.finish()