from puzzlesolver.util import *
from puzzlesolver.solvers import Solver
from puzzlesolver.puzzles import Hanoi
from puzzlesolver import PuzzlePlayer
import queue as q

class GeneralSolver(Solver):

    def __init__(self, puzzle, **kwargs):
        self.remoteness = {}
        self.puzzle = puzzle
    
    def getRemoteness(self, puzzle, **kwargs):
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return PuzzleValue.UNSOLVABLE

    def getValue(self, puzzle, **kwargs):
        remoteness = self.getRemoteness(puzzle, **kwargs)
        if remoteness == PuzzleValue.UNSOLVABLE: return PuzzleValue.UNSOLVABLE
        return PuzzleValue.SOLVABLE

    def solve(self, **kwargs):
        # BFS for remoteness classification
        def helper(self, puzzles):
            queue = q.Queue()
            for puzzle in puzzles: queue.put(puzzle)
            while not queue.empty():
                puzzle = queue.get()
                for move in puzzle.generateMoves():
                    nextPuzzle = puzzle.doMove(move)
                    if hash(nextPuzzle) not in self.remoteness:
                        self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                        queue.put(nextPuzzle)

        ends = self.puzzle.generateSolutions()
        for end in ends: 
            self.remoteness[hash(end)] = 0
        helper(self, ends)

def testTutorial():
    puzzle = Hanoi()
    solver = GeneralSolver(Hanoi())
    solver.solve()
    assert solver.getRemoteness(puzzle) == 7