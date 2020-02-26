from copy import deepcopy
from .Puzzle import Puzzle
from ..util import *
from ..solver.generalsolver import GeneralSolver
from ..puzzleplayer import PuzzlePlayer

class Npuzzle(Puzzle):
    def __init__(self, size=3):
        self.size = size
        # Npuzzle does not have a starting position, but is scrambled.  We'll
        # take starting position to be decreasing with empty space in bottom
        # right corner.
        self.position = range(size**2-1,-1,-1)

    def __str__(self):
        ret = ""
        for i in range(self.size):
            for j in range(self.size):
                ret += (str(self.position[self.size*i + j])) + "\t"
            ret += "\n"
        return ret

    def primitive(self):
        if self.position == [i for i in range(1, size**2)] + [0]:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNSOLVED

    def generateMoves(self):
        return getAdjacent(position.index(0))

    def doMove(self, move):
        moved = self.position[move]
        zeroindex = self.position.index(0)
        self.position[move] = 0
        self.position[zeroindex] = moved
        return self.position

    def getAdjacent(index):
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

if __name__ == "__main__":
    PuzzlePlayer(Npuzzle(size=3), GeneralSolver()).play()
