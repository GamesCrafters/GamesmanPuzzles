from copy import deepcopy
from . import ServerPuzzle
from ..util import *

class LightsOut(ServerPuzzle):

    id      = "lights"
    auth    = "Anthony Ling, Robert Shi"
    name    = "Lights Out"
    desc    = "Click on the squares on the grid to turn it and adjacent squares off. Try to turn off all the squares!"
    date    = "January 14, 2023"

    try:
        from ..extern import m4ri_utils
    except:
        variants = [str(i) for i in range(2, 6)]
        variants_desc = ["{}x{}".format(i, i) for i in range(2, 6)]
        closed_form_variants = []
    else:
        variants = [str(i) for i in range(2, 9)]
        variants_desc = ["{}x{}".format(i, i) for i in range(2, 9)]
        closed_form_variants = ['2', '3', '6', '7', '8']
    test_variants = [str(i) for i in range(2, 5)]
    startRandomized = True

    def __init__(self, variant='3'):
        variant = int(variant)
        self.grid = [[True for _ in range(variant)] for _ in range(variant)]
        self.size = variant

    @property
    def variant(self):
        return str(len(self.grid))

    def __str__(self):
        return "\n".join([str([int(i) for i in row]) for row in self.grid])
    
    def primitive(self):
        for row in self.grid:
            for entry in row:
                if entry == 1: return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE
    
    def doMove(self, move):
        x, y = move[0], move[1]
        puzzle = LightsOut(variant=str(self.size))
        puzzle.grid = deepcopy(self.grid)
        for i in range(max(x - 1, 0), min(self.size, x + 2)):
            puzzle.grid[y][i] = not puzzle.grid[y][i]
        for j in range(max(y - 1, 0), min(self.size, y + 2)):
            puzzle.grid[j][x] = not puzzle.grid[j][x]
        puzzle.grid[y][x] = not puzzle.grid[y][x]
        return puzzle

    def generateMoves(self, movetype="all"):
        if movetype == 'for' and movetype == 'back': return []
        return [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid))]

    def __hash__(self):
        result = ""
        for row in self.grid:
            str_row = [str(int(entry)) for entry in row]
            result += "".join(str_row)
        return int(result, base=2)

    def generateSolutions(self):
        puzzle = LightsOut(variant=self.size)
        puzzle.grid = [[False for _ in range(self.size)] for _ in range(self.size)]
        return [puzzle]

    @classmethod
    def fromHash(cls, variantid, hash_val):
        puzzle = cls(variant=variantid)
        grid_size = puzzle.size * puzzle.size
        hash_str = format(hash_val, "{}b".format(grid_size))
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                puzzle.grid[i][j] = (hash_str[i * puzzle.size + j] == '1')
        return puzzle

    @classmethod
    def generateStartPosition(cls, variantid):
        variant = int(variantid)
        position = "R_{}_{}_{}_".format("A", variant, variant)
        position += '1' * (variant ** 2)
        return cls.fromString(position)

    @classmethod
    def fromString(cls, position: str):
        parts = position.split("_")
        if (len(parts) <= 4): 
            raise ValueError("Invalid position")
        l = int(parts[2])
        w = int(parts[3])
        if (l != w):
            raise TypeError("Unsupported variant")
        position = parts[4]

        variant = int(len(position) ** (1/2))
        if (l != variant):
            raise TypeError("Unsupported variant")
        puzzle = cls(variant=variant)
        puzzle.grid = []
        for i in range(variant):
            row = position[i*variant:(i+1)*variant]
            row = [True if i == '1' else False for i in row]
            puzzle.grid.append(row)
        return puzzle

    def toString(self, mode='minimal'):
        output = "R_{}_{}_{}_".format("A", len(self.grid), len(self.grid[0]))

        result = ""
        for row in self.grid:
            str_row = ["1" if entry else "0" for entry in row]
            result += "".join(str_row)
        output += result
        return output
    
    def moveString(self, move, mode='uwapi'):
        if mode == 'uwapi':
            return f'A_t_{move[0] + move[1] * len(self.grid)}_x'
        else:
            return f"{chr(ord('a') + move[0])}{len(self.grid) - move[1]}"

    def isLegalPosition(self):
        return True
