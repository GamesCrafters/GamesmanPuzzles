from copy import deepcopy
from .Puzzle import Puzzle
from ..util import *
from ..solver.GeneralSolver import GeneralSolver
from ..PuzzlePlayer import PuzzlePlayer

## TODO Fix swap
class Npuzzle(Puzzle):
    def __init__(self, size=3):
        self.size = size
        # Npuzzle does not have a starting position, but is scrambled.  We'll
        # take starting position to be decreasing with empty space in bottom
        # right corner.
        self.position = [i for i in range(1, self.size**2)] + [0] 
        self.position = Npuzzle.swap(self.position, self.size**2 -1, self.size**2-2)

    def __key(self):
        return str(self.position)

    def __hash__(self):
        return hash(self.__key())

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

    def generateMoves(self):
        return self.getAdjacent(self.position.index(0))

    def doMove(self, move):
        newPuzzle = Npuzzle(size=self.size)
        position = deepcopy(self.position)
        zeroindex = position.index(0)
        newPuzzle.position = Npuzzle.swap(position, move, zeroindex)
        return newPuzzle        

    @staticmethod
    def swap(arr, i1, i2):
        temp = arr[i1]
        arr[i1] = arr[i2]
        arr[i2] = temp
        return arr

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
    def generateSolutions(self):
        newPuzzle = Npuzzle(size=self.size)
        newPuzzle.position = [i for i in range(1, self.size**2)] + [0]
        return [newPuzzle]


if __name__ == "__main__":
    PuzzlePlayer(Npuzzle(size=3), GeneralSolver()).play()
