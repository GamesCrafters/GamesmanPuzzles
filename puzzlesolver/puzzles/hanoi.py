"""Game for Tower of Hanoi
https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import IndexSolver

from hashlib import sha1

class Hanoi(ServerPuzzle):

    puzzleid = 'hanoi'
    author = "Anthony Ling"
    puzzle_name = "Tower of Hanoi"
    description = """Move smaller discs ontop of bigger discs. 
        Fill the rightmost stack."""
    date_created = "April 2, 2020"

    variants = {str(i) : IndexSolver for i in range(14, 0, -1)}
    test_variants = {str(i) : IndexSolver for i in range(3, 0, -1)}

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

    @property
    def numPositions(self):
        return 3 ** int(self.variant)

    def __hash__(self):
        # Assign discs to stack num
        num_to_stack = {}
        for entry in self.stacks[2]:
            num_to_stack[entry] = 0

        bigger_stack = 1 if max(self.stacks[0] + [0]) < max(self.stacks[1] + [0]) else 0
        for entry in self.stacks[bigger_stack]:
            num_to_stack[entry] = 1
        
        smaller_stack = 0 if bigger_stack == 1 else 1
        for entry in self.stacks[smaller_stack]:
            num_to_stack[entry] = 2
        
        # Compute hash
        result = 0
        multiply = 1
        for i in range(1, int(self.variant) + 1):
            result += num_to_stack[i] * multiply
            multiply *= 3
        return result

    def __str__(self):
        return str(self.stacks)

    def getName(self):
        return 'Hanoi'

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
    def deserialize(cls, positionid, **kwargs):
        puzzle = Hanoi()
        puzzle.stacks = []
        stacks = positionid.split("-")
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
                
    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        try: puzzle = cls.deserialize(positionid)
        except: return False
        unique = set()
        if len(puzzle.stacks) != 3: return False
        for stack in puzzle.stacks:
            if stack != sorted(stack, reverse=True):
                return False
            unique.update(stack)
        if len(unique) != int(puzzle.variant) or min(unique) != 1 or max(unique) != int(puzzle.variant):
            return False
        return True
