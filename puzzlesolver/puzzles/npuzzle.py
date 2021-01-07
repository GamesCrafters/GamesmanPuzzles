"""Game for 15 puzzle, generalized to N x N
https://en.wikipedia.org/wiki/15_puzzle
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import *

import math

class Npuzzle(ServerPuzzle):
    
    puzzleid = 'npuzzle'
    author = "Arturo Olvera"
    name = "N x N '15'-puzzle"
    description = "Shift pieces to get puzzle in ascending order."
    date_created = "April 10, 2020"
    
    variants = {str(i) : IndexSolver for i in range(2, 4)}
    test_variants = {"2" : IndexSolver}

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
        h = 0
        for i in self.position:
            h += i
            h *= len(self.position)
        return h

    def __str__(self):
        ret = ""
        for i in range(self.size):
            for j in range(self.size):
                ret += (str(self.position[self.size*i + j])) + "\t"
            ret += "\n"
        return ret

    def getName(self):
        return self.variant + '-puzzle' 

    def primitive(self):
        if self.position == [i for i in range(1, self.size**2)] + [0]:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def doMove(self, move):
        newPuzzle = Npuzzle(size=self.size)
        position = deepcopy(self.position)
        zeroindex = position.index(0)
        moveindex = position.index(move)
        newPuzzle.position = Npuzzle.swap(position, moveindex, zeroindex)
        return newPuzzle        

    def generateMoves(self, movetype='bi'):
        if movetype == 'for':
            return []
        adjacent = self.getAdjacent(self.position.index(0))
        return [self.position[a] for a in adjacent]

    def generateSolutions(self):
        newPuzzle = Npuzzle(size=self.size)
        newPuzzle.position = [i for i in range(1, self.size**2)] + [0]
        return [newPuzzle]

    @staticmethod
    def swap(arr, i1, i2):
        arr[i1], arr[i2] = arr[i2], arr[i1]
        return arr

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Npuzzle.variants: raise IndexError("Out of bounds variantid")
        return Npuzzle(size=int(variantid))

    @classmethod
    def deserialize(cls, puzzleid, **kwargs):
        try:
            puzzle = Npuzzle()
            puzzle.position = [int(i) for i in puzzleid.split('-')]
            puzzle.size = int(math.sqrt(len(puzzle.position)))
            return puzzle
        except:
            raise PuzzleException("Invalid puzzleid")

    def serialize(self, **kwargs):
        return '-'.join([str(x) for x in self.position])

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
        puzzle = cls.deserialize(positionid)
        if len(puzzle.position) != puzzle.size ** 2:
            raise PuzzleException("Incorrect puzzle length.")

        for i in range(puzzle.size ** 2):
            if puzzle.position.count(i) != 1:
                raise PuzzleException("Incorrect pieces.")

        return True            
