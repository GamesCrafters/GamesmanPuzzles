"""Game for Tower of Hanoi
https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""

from copy import deepcopy
from .Puzzle import Puzzle
from ..util import *
from ..solver.GeneralSolver import GeneralSolver
from ..PuzzlePlayer import PuzzlePlayer

class Hanoi(Puzzle):

    def __init__(self, size=3):
        self.size = size
        self.stacks = [
            list(range(size, 0, -1)),
            [],
            []
        ]
    
    def __key(self):
        return (str(self.stacks))

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.stacks)

    def primitive(self):
        if self.stacks[2] == list(range(self.size, 0, -1)):
            return PuzzleValue.SOLVABLE 
        return GameValue.UNDECIDED

    def doMove(self, move):
        newPuzzle = Hanoi(size=self.size)
        stacks = deepcopy(self.stacks)
        stacks[move[1]].append(stacks[move[0]].pop())
        newPuzzle.stacks = stacks
        return newPuzzle        

    def generateMoves(self):
        moves = []
        for i, stack1 in enumerate(self.stacks):
            if not stack1: continue
            for j, stack2 in enumerate(self.stacks):
                if i == j: continue
                if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
        return moves

    def winStates(self):
        newPuzzle = Hanoi(size=self.size)
        newPuzzle.stacks = [
            [],
            [],
            list(range(self.size, 0, -1))
        ]
        return [newPuzzle]

if __name__ == "__main__":
    PuzzlePlayer(Hanoi(size=7), GeneralSolver(), auto=True).play()