
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI

class HF(Puzzle):
    id = 'HF'

    def __init__(self, **kwargs):
        self.start = kwargs.get('start', 4)
        self.pos = self.start
    
    def toString(self, **kwargs):
        return str(self.pos)

    def primitive(self, **kwargs):
        if self.pos == 0:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def generateMoves(self, movetype='all'):
        if self.pos != 0 and self.pos % 3 == 0:
            return [(-1,)]
        elif self.pos >= self.start:
            return [(1,), (2,)]
            
        if (self.pos + 2) % 3 == 0:
            return [(-1,), (1,)] if self.pos % 4 == 1 else [(-1,), (1,), (2,)]
        elif (self.pos + 1) % 3 == 0:
            return [(-2,), (1,)] if self.pos % 4 == 1 else [(-2,), (1,), (2,)]

        return [(-2,), (-1,), (1,), (2,)]
    
    def doMove(self, move, **kwargs):
        nP = HF(start=self.start)
        position = self.pos
        position -= move[0]
        nP.pos = position
        return nP
    
    def __hash__(self):
        return self.pos

puzzle = HF()
TUI(puzzle, solver=GeneralSolver(puzzle), info=True).play()
