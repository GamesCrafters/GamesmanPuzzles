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
        self.stacks = [
            [3, 2, 1],
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
        return GameValue.WIN if self.stacks[2] == [3, 2, 1] else GameValue.UNDECIDED

    def doMove(self, move):
        newPuzzle = Hanoi()
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
        newPuzzle = Hanoi()
        newPuzzle.stacks = [
            [],
            [],
            [3, 2, 1]
        ]
        return [newPuzzle]

if __name__ == "__main__":
    PuzzlePlayer(Hanoi(), GeneralSolver()).play()