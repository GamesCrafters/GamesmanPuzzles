"""
File: lightsout.py
Puzzle: Lights Out
Author: Anthony Ling (v0), Robert Shi (v1, AutoGUI), Anthony Dokanchi (v2, closed-form solver for any size)
Date: January 14, 2023
"""

from . import ServerPuzzle
from ..util import *
from ..solvers.lightsoutclosedformsolver import getMath

MIN_SIZE = 2
MAX_SIZE = 38

class LightsOut(ServerPuzzle):

    id = "lightsout"

    variants = [str(i) for i in range(MIN_SIZE, MAX_SIZE + 1)]
    closed_form_variants = variants
    startRandomized = True

    def __init__(self, variant='3'):
        size = int(variant)
        self.size = size
        # rows[y] is an int whose bit x is cell (x, y); 1 means lit.
        self.rows = [(1 << size) - 1] * size

    @property
    def grid(self):
        """The board as rows of booleans, grid[y][x]."""
        return [[bool(row >> x & 1) for x in range(self.size)] for row in self.rows]

    @grid.setter
    def grid(self, grid):
        self.rows = [sum(1 << x for x, entry in enumerate(row) if entry) for row in grid]

    @property
    def variant(self):
        return str(self.size)

    def __str__(self):
        return "\n".join([str([int(i) for i in row]) for row in self.grid])

    def primitive(self):
        if any(self.rows):
            return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE

    def doMove(self, move):
        x, y = move[0], move[1]
        puzzle = LightsOut(variant=self.size)
        rows = list(self.rows)
        rows[y] ^= ((7 << x) >> 1) & ((1 << self.size) - 1)
        if y > 0:
            rows[y - 1] ^= 1 << x
        if y < self.size - 1:
            rows[y + 1] ^= 1 << x
        puzzle.rows = rows
        return puzzle

    def generateMoves(self, movetype="all"):
        # Every move undoes itself, so every move is legal in every direction.
        return [(i, j) for i in range(self.size) for j in range(self.size)]

    def __hash__(self):
        return int(self.toString(StringMode.HUMAN_READABLE), base=2)

    def generateSolutions(self):
        puzzle = LightsOut(variant=self.size)
        puzzle.rows = [0] * self.size
        return [puzzle]

    @classmethod
    def fromHash(cls, variantid, hash_val):
        puzzle = cls(variant=variantid)
        grid_size = puzzle.size * puzzle.size
        return cls._fromBits(puzzle.size, format(hash_val, "0{}b".format(grid_size)))

    @classmethod
    def generateStartPosition(cls, variantid):
        variant = int(variantid)
        return cls.fromString(variantid, '1' * (variant ** 2))

    @classmethod
    def fromString(cls, variant_id, position: str):
        """Raises TypeError for an unsupported variant or a non-string position,
        and ValueError for a position that is malformed or cannot be solved."""
        if str(variant_id) not in LightsOut.variants:
            raise TypeError("Unsupported variant")
        if not isinstance(position, str):
            raise TypeError("PositionID must be type str")
        size = int(variant_id)
        if len(position) != size * size:
            raise ValueError("Position has the wrong length for this variant")
        if position.strip('01'):
            raise ValueError("Position may only contain 0 and 1")
        puzzle = cls._fromBits(size, position)
        if not getMath(size).isSolvable(puzzle.rows):
            raise ValueError("Position cannot be solved")
        return puzzle

    @classmethod
    def _fromBits(cls, size, bits):
        """Builds a puzzle from a string of size * size '0'/'1' characters."""
        puzzle = cls(variant=size)
        puzzle.rows = [int(bits[y * size:(y + 1) * size][::-1], 2) for y in range(size)]
        return puzzle

    def toString(self, mode):
        result = '1_' if mode == StringMode.AUTOGUI else ''
        width = "0{}b".format(self.size)
        return result + ''.join(format(row, width)[::-1] for row in self.rows)

    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return f'A_t_{move[0] + move[1] * self.size}_x'
        else:
            return f"{self._columnName(move[0])}{self.size - move[1]}"

    @staticmethod
    def _columnName(x):
        """Spreadsheet-style column names: a, b, ..., z, aa, ab, ..."""
        name = ''
        x += 1
        while x:
            x, letter = divmod(x - 1, 26)
            name = chr(ord('a') + letter) + name
        return name

    def isLegalPosition(self):
        return True
