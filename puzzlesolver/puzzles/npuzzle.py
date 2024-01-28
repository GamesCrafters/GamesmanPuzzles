"""
File: npuzzle.py
Puzzle: N-Puzzle (Sliding Number Puzzle)
Author: Arturo Olvera (Backend), Cameron Cheung (AutoGUI)
Date: April 10, 2020
"""

"""Game for 15 puzzle, generalized to N x N
https://en.wikipedia.org/wiki/15_puzzle
"""

from . import ServerPuzzle
from ..util import *
from ..solvers import *
import math

class Npuzzle(ServerPuzzle):
    
    id = 'npuzzle'
    
    variants = [str(i) for i in range(3, 4)]
    startRandomized = True

    def __init__(self, size=3):
        if not isinstance(size,int): raise ValueError
        self.size = size
        # Npuzzle does not have a starting position, but is scrambled instead.
        # This is a default scramble
        self.position = [i for i in range(1, self.size**2)] + [0] 
        self.position = Npuzzle.swap(self.position, self.size**2 -1, self.size**2-2)

    @property
    def variant(self):
        return str(self.size)

    def __hash__(self):
        board_size = self.size * self.size
        h = 0
        col_ids = list(range(board_size))
        for i in range(board_size):
            h += col_ids.index(self.position[i]) * math.factorial(board_size - i - 1)
            col_ids.remove(self.position[i])
        return h

    def __str__(self):
        ret = ""
        for i in range(self.size):
            for j in range(self.size):
                ret += (str(self.position[self.size*i + j])) + "\t"
            ret += "\n"
        return ret

    def primitive(self):
        if self.position == [i for i in range(1, self.size**2)] + [0]:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def doMove(self, move):
        newPuzzle = Npuzzle(size=self.size)
        newPuzzle.position = Npuzzle.swap(self.position[:], move[0], move[1])
        return newPuzzle

    def generateMoves(self, movetype='bi'):
        if movetype == 'for':
            return []
        index_0 = self.position.index(0)
        adjacent = self.getAdjacent(index_0)
        return [(a, index_0) for a in adjacent]

    def generateSolutions(self):
        newPuzzle = Npuzzle(size=self.size)
        newPuzzle.position = [i for i in range(1, self.size**2)] + [0]
        return [newPuzzle]

    @staticmethod
    def swap(arr, i1, i2):
        arr[i1], arr[i2] = arr[i2], arr[i1]
        return arr

    @classmethod
    def fromHash(cls, variantid, hash_val):
        puzzle = cls(int(variantid))
        board_size = puzzle.size**2
        col_ids = list(range(board_size))
        position = []
        for r in range(board_size - 1, -1, -1):
            f = math.factorial(r)
            position.append(col_ids.pop(hash_val // f))
            hash_val %= f
        puzzle.position = position
        return puzzle

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Npuzzle.variants: raise IndexError("Out of bounds variantid")
        return Npuzzle(size=int(variantid))

    @classmethod
    def fromString(cls, variant_id, puzzleid):
        try:
            puzzleid = puzzleid.split('_')[-1]
            puzzle = Npuzzle()
            puzzle.position = [int(i) if i != '-' else 0 for i in puzzleid]
            puzzle.size = int(variant_id)
            return puzzle
        except Exception as _:
            raise PuzzleException('Invalid puzzleid')
    
    def toString(self, mode):
        prefix = '1_' if mode == StringMode.AUTOGUI else ''
        return prefix + ''.join([str(x) if int(x) != 0 else '-' for x in self.position])
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return f'M_{move[0]}_{move[1]}_x'
        else:
            return str(self.position[move[0]])

    def getAdjacent(self, index):
        adj = []
        right = index + 1
        left = index - 1
        up = index - self.size
        down = index + self.size
        if not right % self.size == 0:
            adj.append(right)
        if not left % self.size == self.size - 1:
            adj.append(left)
        if not up < 0:
            adj.append(up)
        if not down > self.size**2 - 1:
            adj.append(down)
        return adj

    def invCount(self):
        inv = 0
        ind = lambda x: self.position.index(x)
        for i in range(self.size**2 - 1):
            for j in range(i+1, self.size**2):
                if (ind(i) < ind(j) and self.position[i] > self.position[j]):
                    inv += 1
        return inv

    def findBlankRow(self):
        return self.size - (self.position.index(0) // self.size)

    @classmethod
    def isLegalPosition(cls, positionid):
        puzzle = cls.fromString(positionid)
        if len(puzzle.position) != puzzle.size ** 2:
            raise PuzzleException("Incorrect puzzle length.")

        for i in range(puzzle.size ** 2):
            if puzzle.position.count(i) != 1:
                raise PuzzleException("Incorrect pieces.")

        return True            
