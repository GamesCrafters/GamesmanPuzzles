from . import ServerPuzzle
from ..solvers import SqliteSolver
from ..util import *

class LightsOut(ServerPuzzle):

    puzzleid = "lightsout"
    author = "Anthony Ling"
    puzzle_name = "Lights Out"
    description = "Meh"
    date_created = "April 6, 2020"

    variants = {
        '2': SqliteSolver,
        '3': SqliteSolver,
        '4': SqliteSolver
    }

    def __init__(self, variant=3, **kwargs):
        self.grid = [[True for _ in range(variant)] for _ in range(variant)]
        self.size = variant

    @property
    def variant(self):
        return str(len(self.grid))

    def __str__(self):
        return "/n".join([str(row)for row in self.grid])
    
    def primitive(self, **kwargs):
        for row in self.grid:
            for entry in row:
                if entry == 1: return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE
    
    def doMove(self, move, **kwargs):
        from copy import deepcopy
        x, y = move[0], move[1]
        puzzle = LightsOut()
        puzzle.grid = deepcopy(self.grid)
        for i in range(max(x - 1, 0), min(len(self.grid), x + 1)):
            for j in range(max(y - 1, 0), min(len(self.grid), y + 1)):
                puzzle.grid[i][j] = not puzzle.grid[i][j]
        return puzzle

    def generateMoves(self, movetype="all", **kwargs):
        if movetype == 'for' and movetype == 'back': return []
        moves = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                moves.append((i, j))
        return moves

    def __hash__(self):
        return int(self.serialize())

    def generateSolutions(self, **kwargs):
        puzzle = LightsOut(variant=self.size)
        puzzle.grid = [[False for _ in range(self.size)] for _ in range(self.size)]
        return [puzzle]

    @classmethod
    def deserialize(cls, position, **kwargs):
        length, variant = len(position), int(len(position) ** (1/2))
        puzzle = cls(variant=variant)
        puzzle.grid = []
        row = []
        while length > 0:
            row.append(position[len(position) - length])
            if len(row) == variant:
                puzzle.grid.append(row)
                row = []
            length-=1
        return puzzle

    def serialize(self, **kwargs):
        result = ""
        for row in self.grid:
            str_row = [str(int(entry)) for entry in row]
            result += "".join(str_row)
        return result

    def isLegalPosition(self):
        return True