"""
File: lightsout.py
Puzzle: Lights Out
Author: Anthony Ling (v0), Robert Shi (v1, AutoGUI)
Date: January 14, 2023
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *

class LightsOut(ServerPuzzle):

    id = "lightsout"

    try:
        from ..extern import m4ri_utils
    except:
        variants = [str(i) for i in range(2, 6)]
        closed_form_variants = []
    else:
        variants = [str(i) for i in range(2, 9)]
        closed_form_variants = ['2', '3', '6', '7', '8']
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
        return cls.fromString(variantid, '1' * (variant ** 2))

    @classmethod
    def fromString(cls, variant_id, position: str):
        variant = int(variant_id)
        if str(variant) not in LightsOut.variants:
            raise TypeError("Unsupported variant")
        puzzle = cls(variant=variant)
        puzzle.grid = []
        for i in range(variant):
            row = position[i*variant:(i+1)*variant]
            row = [True if i == '1' else False for i in row]
            puzzle.grid.append(row)
        return puzzle

    def toString(self, mode):
        result = '1_' if mode == StringMode.AUTOGUI else ''
        for row in self.grid:
            str_row = ['1' if entry else '0' for entry in row]
            result += ''.join(str_row)
        return result
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return f'A_t_{move[0] + move[1] * len(self.grid)}_x'
        else:
            return f"{chr(ord('a') + move[0])}{len(self.grid) - move[1]}"

    def isLegalPosition(self):
        return True
