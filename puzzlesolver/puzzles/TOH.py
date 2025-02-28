from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI

from puzzlesolver.puzzles import ServerPuzzle


class TOH(ServerPuzzle):
    id = 'toh'
    variants = ["1", "2", "3"]


    def __init__(self, size=3, **kwargs):
        self.stacks = [
            list(range(size, 0, -1)),
            [],
            []
        ]
        
    def toString(self, **kwargs):
        result = []
        for stack in self.stacks:
            result.append("_".join(str(x) for x in stack))
        return "-".join(result)
    
    @classmethod
    def fromString(cls, positionid, **kwargs):
        # Checking if the positionid is a str
        if not isinstance(positionid, str):
            raise TypeError("PositionID is not type str")
        
        # Checking if the string can be split into 3 stacks
        stacks = positionid.split("-")
        if not stacks or len(stacks) != 3:
            raise ValueError("PositionID cannot be translated into Puzzle")
        
        puzzle = TOH()
        puzzle.stacks = []
        seen = set()
        
        try:        
            for string in stacks:
                if string != "":
                    # Check that all disks are ints
                    stack = [int(x) for x in string.split("_")]
                    # Check for duplicate disks
                    if seen.intersection(stack): raise ValueError
                    seen = seen.union(stack)                
                    puzzle.stacks.append(stack)
                else: puzzle.stacks.append([])        
        except ValueError:
            raise ValueError("PositionID cannot be translated into Puzzle")
    
        return puzzle   

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in TOH.variants: raise ValueError("Out of bounds variantid")
        return TOH(size=int(variantid))
        
    def primitive(self, **kwargs):
        if self.stacks[2] == [3, 2, 1]:
            return PuzzleValue.SOLVABLE 
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype="all"):
        if movetype=='for' or movetype=='back': return []
        moves = []
        for i, stack1 in enumerate(self.stacks):
            if not stack1: continue
            for j, stack2 in enumerate(self.stacks):
                if i == j: continue
                if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
        return moves

    def doMove(self, move, **kwargs):
        if (
            not isinstance(move, tuple)
            or len(move) != 2
            or not isinstance(move[0], int)
            or not isinstance(move[1], int)
        ):
            raise TypeError
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = TOH()
        stacks = deepcopy(self.stacks)
        stacks[move[1]].append(stacks[move[0]].pop())
        newPuzzle.stacks = stacks
        return newPuzzle   
        
    def __hash__(self):
        from hashlib import sha1
        h = sha1()
        h.update(str(self.stacks).encode())
        return int(h.hexdigest(), 16)

    def generateSolutions(self, **kwargs):
        newPuzzle = TOH(size=int(self.variant))
        newPuzzle.stacks = [
            [],
            [],
            list(range(int(self.variant), 0, -1))
        ]
        return [newPuzzle]
    
    @property
    def variant(self):
        size = 0
        for stack in self.stacks:
            size += len(stack)
        return str(size)
        