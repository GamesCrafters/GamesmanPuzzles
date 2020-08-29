"""Game for Tower of Hanoi
https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import *
from ..puzzleplayer import PuzzlePlayer

from hashlib import sha1

class Hanoi(ServerPuzzle):

    puzzleid = 'hanoi'
    author = "Anthony Ling"
    puzzle_name = "Tower of Hanoi"
    description = """Move smaller discs ontop of bigger discs. 
        Fill the rightmost stack."""
    date_created = "April 2, 2020"

    variants = {str(i) : SqliteSolver for i in range(1, 11)}

    def __init__(self, size=3, **kwargs):
        if not isinstance(size, int): raise ValueError 
        self.stacks = [
            list(range(size, 0, -1)),
            [],
            []
        ]   
    
    @property
    def variant(self):
        size = 0
        for stack in self.stacks:
            size += len(stack)
        return str(size)

    def __hash__(self):
        # We're being really lazy here and using built in hashlib functions.
        # Can't use regular hash because those are random
        h = sha1()
        h.update(str(self.stacks).encode())
        return int(h.hexdigest(), 16)

    def __str__(self):
        return str(self.stacks)

    def getName(self):
        return 'Hanoi' + self.variant

    def primitive(self, **kwargs):
        if self.stacks[2] == list(range(int(self.variant), 0, -1)):
            return PuzzleValue.SOLVABLE 
        return PuzzleValue.UNDECIDED

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = Hanoi(size=int(self.variant))
        stacks = deepcopy(self.stacks)
        stacks[move[1]].append(stacks[move[0]].pop())
        newPuzzle.stacks = stacks
        return newPuzzle        

    def generateMoves(self, movetype="all", **kwargs):
        if movetype=='for' or movetype=='back': return []
        moves = []
        for i, stack1 in enumerate(self.stacks):
            if not stack1: continue
            for j, stack2 in enumerate(self.stacks):
                if i == j: continue
                if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
        return moves

    def generateSolutions(self, **kwargs):
        newPuzzle = Hanoi(size=int(self.variant))
        newPuzzle.stacks = [
            [],
            [],
            list(range(int(self.variant), 0, -1))
        ]
        return [newPuzzle]

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Hanoi.variants: raise IndexError("Out of bounds variantid")
        return Hanoi(size=int(variantid))
                  
    @classmethod
    def deserialize(cls, puzzleid, **kwargs):
        puzzle = Hanoi()
        puzzle.stacks = []
        stacks = puzzleid.split("-")
        for string in stacks:
            if string != "":
                stack = [int(x) for x in string.split("_")]
                puzzle.stacks.append(stack)
            else: puzzle.stacks.append([])
        return puzzle
    
    def serialize(self, **kwargs):
        result = []
        for stack in self.stacks:
            result.append("_".join(str(x) for x in stack))
        return "-".join(result)
                
    def isLegalPosition(self):
        unique = set()
        if len(self.stacks) != 3: raise PuzzleException("Number of stacks does not equal 3")
        for stack in self.stacks:
            if stack != sorted(stack, reverse=True):
                return False
            unique.update(stack)
        if len(unique) != int(self.variant) or min(unique) != 1 or max(unique) != int(self.variant):
            return False
        return True

if __name__ == "__main__":
    puzzle = Hanoi(size=9)
    PuzzlePlayer(puzzle, SqliteSolver(puzzle=puzzle)).play()
