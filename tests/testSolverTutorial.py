from puzzlesolver.solver.Solver import Solver
from puzzlesolver.util import *
from puzzlesolver.puzzles.Hanoi import Hanoi
from puzzlesolver.PuzzlePlayer import PuzzlePlayer
import queue as q

class GeneralSolver(Solver):
    def __init__(self, *args, **kwargs):
        self.values = {}
        self.remoteness = {}

    def getRemoteness(self, puzzle):
        self.solve(puzzle)
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        return PuzzleValue.UNSOLVABLE

    def solve(self, puzzle):
        if hash(puzzle) in self.values: self.values[hash(puzzle)]        
        def helper(self, puzzle):
            queue = q.Queue()
            queue.put(puzzle)
            while not queue.empty():
                puzzle = queue.get()
                for move in puzzle.generateMoves():
                    nextPuzzle = puzzle.doMove(move)
                    if hash(nextPuzzle) not in self.remoteness:
                        self.values[hash(nextPuzzle)] = PuzzleValue.SOLVABLE
                        self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                        queue.put(nextPuzzle)

        ends = puzzle.winStates()
        for end in ends: 
            self.values[hash(end)] = PuzzleValue.SOLVABLE
            self.remoteness[hash(end)] = 0
            helper(self, end)
        if hash(puzzle) not in self.values: self.values[hash(puzzle)] = PuzzleValue.UNSOLVABLE
        return self.values[hash(puzzle)]

def testTutorial():
    puzzle = Hanoi()
    solver = GeneralSolver()
    solver.solve(puzzle)
    assert solver.getRemoteness(puzzle) == 7