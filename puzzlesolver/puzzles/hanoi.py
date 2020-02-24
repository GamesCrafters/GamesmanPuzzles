"""Game for Tower of Hanoi
https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""

from copy import deepcopy
from .puzzle import Puzzle
from ..util import *
from ..solvers import GeneralSolver
from ..puzzleplayer import PuzzlePlayer

class Hanoi(Puzzle):

    def __init__(self, position_id=None, variant_id=None, size=3, id=None):
        if position_id: self.decode(position_id)
        elif id: self.decode(id)
        else:
            self.size = int(variant_id) if variant_id else size
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

    """ Removed until it's proved that its necessary
    def __eq__(self, other):
        return self.stacks == other.stacks
    """

    def getName(self):
        return 'Hanoi' + str(self.size)

    def encode(self):
        id = ""
        for i, stack in enumerate(self.stacks):
            for j, disc in enumerate(stack):
                id += str(disc)
                if j != len(stack) - 1: id += "a"
            if i != len(self.stacks) - 1: id += "b"
        return id

    # Helper function for decoding, not necessary
    def decode(self, id):
        id = str(id)
        stacks = id.split("b")
        if not len(stacks) == 3: raise ValueError
        self.stacks = []
        self.size = 0
        for stack in stacks:
            if not stack: 
                self.stacks.append([])
                continue
            discs = stack.split("a")
            discs = [int(disc) for disc in discs]
            if not all(discs[i] > discs[i+1] for i in range(len(discs) - 1)):
                raise ValueError
            self.stacks.append(discs)
            self.size += len(discs)

    def primitive(self):
        if self.stacks[2] == list(range(self.size, 0, -1)):
            return PuzzleValue.SOLVABLE 
        return PuzzleValue.UNDECIDED

    def doMove(self, move):
        if move not in self.generateMoves(): raise ValueError
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

    def generateSolutions(self):
        newPuzzle = Hanoi(size=self.size)
        newPuzzle.stacks = [
            [],
            [],
            list(range(self.size, 0, -1))
        ]
        return [newPuzzle]

    @staticmethod
    def checkValidVariant(position_id, variant_id):
        size = int(variant_id)
        puzzle = Hanoi(id=position_id)
        if puzzle.size != size: return False
        return True

if __name__ == "__main__":
    puzzle = Hanoi(size=3)
    PuzzlePlayer(puzzle, GeneralSolver(puzzle=puzzle)).play()
