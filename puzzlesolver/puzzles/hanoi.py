"""Game for Tower of Hanoi
https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""

from copy import deepcopy
from .puzzle import Puzzle
from ..util import *
from ..solvers import GeneralSolver
from ..puzzleplayer import PuzzlePlayer

class Hanoi(Puzzle):

    def __init__(self, size=3, **kwargs):
        self.size = size
        if not isinstance(self.size, int): raise ValueError 
        self.stacks = [
            list(range(self.size, 0, -1)),
            [],
            []
        ]
    
    def __key(self):
        return (str(self.stacks))

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.stacks)

    def getName(self):
        return 'Hanoi' + str(self.size)

    def primitive(self, **kwargs):
        if self.stacks[2] == list(range(self.size, 0, -1)):
            return PuzzleValue.SOLVABLE 
        return PuzzleValue.UNDECIDED

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = Hanoi(size=self.size)
        stacks = deepcopy(self.stacks)
        stacks[move[1]].append(stacks[move[0]].pop())
        newPuzzle.stacks = stacks
        return newPuzzle        

    def generateMoves(self, movetypes="all", **kwargs):
        moves = []
        for i, stack1 in enumerate(self.stacks):
            if not stack1: continue
            for j, stack2 in enumerate(self.stacks):
                if i == j: continue
                if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
        return moves

    def generateSolutions(self, **kwargs):
        newPuzzle = Hanoi(size=self.size)
        newPuzzle.stacks = [
            [],
            [],
            list(range(self.size, 0, -1))
        ]
        return [newPuzzle]

if __name__ == "__main__":
    puzzle = Hanoi(size=3)
    PuzzlePlayer(puzzle, GeneralSolver(puzzle=puzzle)).play()
