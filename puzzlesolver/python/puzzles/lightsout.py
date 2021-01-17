from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import IndexSolver

class LightsOut(ServerPuzzle):

    puzzleid = "lights"
    author = "Anthony Ling"
    name = "Lights Out"
    description = "Meh"
    date_created = "April 6, 2020"

    variants = { str(i) : IndexSolver for i in range(2, 5)}

    def __init__(self, variant='3', **kwargs):
        variant = int(variant)
        self.grid = [[True for _ in range(variant)] for _ in range(variant)]
        self.size = variant

    @property
    def variant(self):
        return str(len(self.grid))

    def __str__(self):
        return "\n".join([str([int(i) for i in row]) for row in self.grid])
    
    def primitive(self, **kwargs):
        for row in self.grid:
            for entry in row:
                if entry == 1: return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE
    
    def doMove(self, move, **kwargs):
        from copy import deepcopy
        x, y = move[0], move[1]
        puzzle = LightsOut(variant=str(self.size))
        puzzle.grid = deepcopy(self.grid)
        for i in range(max(x - 1, 0), min(self.size, x + 2)):
            puzzle.grid[y][i] = not puzzle.grid[y][i]
        for j in range(max(y - 1, 0), min(self.size, y + 2)):
            puzzle.grid[j][x] = not puzzle.grid[j][x]
        puzzle.grid[y][x] = not puzzle.grid[y][x]
        return puzzle

    def generateMoves(self, movetype="all", **kwargs):
        if movetype == 'for' and movetype == 'back': return []
        moves = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                moves.append((i, j))
        return moves

    def __hash__(self):
        result = int(self.serialize(), 2)
        return result

    def generateSolutions(self, **kwargs):
        puzzle = LightsOut(variant=self.size)
        puzzle.grid = [[False for _ in range(self.size)] for _ in range(self.size)]
        return [puzzle]

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        variant = int(variantid)
        position = '1' * (variant ** 2)
        return cls.deserialize(position)

    @classmethod
    def deserialize(cls, position, **kwargs):
        variant = int(len(position) ** (1/2))
        puzzle = cls(variant=variant)
        puzzle.grid = []
        for i in range(variant):
            row = position[i*variant:(i+1)*variant]
            row = [bool(int(i)) for i in row]
            puzzle.grid.append(row)
        return puzzle

    def serialize(self, **kwargs):
        result = ""
        for row in self.grid:
            str_row = [str(int(entry)) for entry in row]
            result += "".join(str_row)
        return result

    def isLegalPosition(self):
        return True