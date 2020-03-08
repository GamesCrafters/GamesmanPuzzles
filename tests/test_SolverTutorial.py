from puzzlesolver.solvers.solver import Solver
from puzzlesolver.util import *
from puzzlesolver.puzzles.hanoi import Hanoi
from puzzlesolver.puzzleplayer import PuzzlePlayer
import queue as q

class GeneralSolver(Solver):

    def __init__(self, **kwargs):
        self.values = {}
        self.remoteness = {}
    
    def getRemoteness(self, puzzle, **kwargs):
        self.solve(puzzle)
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return PuzzleValue.UNSOLVABLE

    def solve(self, puzzle, **kwargs):
        if hash(puzzle) in self.values: return self.values[hash(puzzle)]
        
        # BFS for remoteness classification
        def helper(self, puzzles):
            queue = q.Queue()
            for puzzle in puzzles: queue.put(puzzle)
            while not queue.empty():
                puzzle = queue.get()
                for move in puzzle.generateMoves():
                    nextPuzzle = puzzle.doMove(move)
                    if hash(nextPuzzle) not in self.remoteness:
                        self.values[hash(nextPuzzle)] = PuzzleValue.SOLVABLE
                        self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                        queue.put(nextPuzzle)

        ends = puzzle.generateSolutions()
        for end in ends: 
            self.values[hash(end)] = PuzzleValue.SOLVABLE
            self.remoteness[hash(end)] = 0
        helper(self, ends)
        if hash(puzzle) not in self.values: self.values[hash(puzzle)] = PuzzleValue.UNSOLVABLE
        return self.values[hash(puzzle)]

def testTutorial():
    puzzle = Hanoi()
    solver = GeneralSolver()
    solver.solve(puzzle)
    assert solver.getRemoteness(puzzle) == 7