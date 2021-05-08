"""N Queens Puzzle
 https://en.wikipedia.org/wiki/Eight_queens_puzzle
"""

from copy import deepcopy
from puzzlesolver.puzzles._models import ServerPuzzle
from puzzlesolver.util import *
from puzzlesolver.solvers import IndexSolver

import math


class NQueens(ServerPuzzle):

    id = 'nqueens'
    auth = 'Mia Campdera-Pulido'
    name = 'N queens puzzle'
    desc = 'Place the N queens in a way such that they do not attack each other'
    date = 'March 17, 2021'

    variants = ['4', '5', '6', '7', '8']
    test_variants = ["4"]

    def __init__(self, variantid=None):
        """Returns the starting position of nqueens based on the variant
        Input:(Optional) variantid - str
        Output: A N queens puzzle
        """

        self.size = 4

        if variantid:
            if not isinstance(variantid, str):
                raise TypeError("VariantID is not type str")
            int_variant_id = int(variantid)
            if int_variant_id > 8 or int_variant_id < 4:
                raise ValueError("Invalid variantID")

            self.size = int_variant_id

        self.board = [0 for x in range(self.size * self.size)]

    @property
    def variant(self):
        return str(self.size)

    @property
    def numPositions(self):
        """Returns the upperbound number of possible hashes
        Output: numPositions - int
        """
        n = self.size * self.size
        k = self.size
        return int(math.factorial(n) / (math.factorial(n-k) * math.factorial(k)))

    def __hash__(self):
        h = ""
        for ele in self.board:
            h += str(ele)
        return int(h)

    def toString(self, mode='minimal'):
        """Returns the string representation of the Puzzle based on the type.
        Inputs:
            'minimal' mode: returns serialize() version
            'complex' mode: returns printInfo() version
        Output: String representation
        """
        str1 = ""
        for ele in self.board:
            str1 += str(ele)
        list_board = ["q" if ele == '1' else "-" for ele in str1]
        lst_str = ''
        for ele in list_board:
            lst_str += ele
        if mode == 'minimal':
            return "R_{}_{}_{}_".format("A", self.size, self.size) + lst_str
        elif mode == 'complex':
            col = 0
            str2 = ''
            for i in range(self.size):
                str3 = lst_str[col:col + self.size]
                str2 += "{}\n".format(str3)
                col += self.size
            return str2

    @classmethod
    def fromString(cls, positionid):
        board = positionid[8:]
        if not isinstance(positionid, str):
            raise TypeError("PositionID is not type str")
        a = math.sqrt(len(board))

        if a > int(a):
            raise ValueError("PositionID cannot be translated into Puzzle")

        board_list = []
        board = positionid[8:]
        for i in range(len(board)):
            board_list += [board[i:i + 1]]
        board = [1 if ele == 'q' else 0 for ele in board_list]
        variantid = str(int(math.sqrt(len(positionid))))
        new_board = NQueens(variantid)
        new_board.board = board
        return new_board

    def __repr__(self):
        """"Returns the string representation of the Puzzle as a
        Python object
        """
        return self.toString('complex')

    def primitive(self):
        """If the Puzzle is at an endstate, return PuzzleValue.SOLVABLE or PuzzleValue.UNSOLVABLE
        else return PuzzleValue.UNDECIDED
        PuzzleValue located in the util class. If you're in the puzzles or solvers directory
        you can write from ..util import *
        Outputs:
            Primitive of Puzzle type PuzzleValue
        """
        if self.check_win():
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def doMove(self, move):
        """Given a valid move, returns a new Puzzle object with that move executed.
        Does nothing to the original Puzzle object
        Input: Move - 'all'
        Output: Puzzle with move executed
        """
        if not isinstance(move, str):
            raise TypeError("Invalid type for move")
        if move not in self.generateMoves():
            raise ValueError("Move not possible")

        new_board = NQueens(str(self.size))
        board = self.board[:]
        parts = move.split("_")
        i = int(parts[2])
        board[i] = 1
        new_board.board = board
        return new_board

    @classmethod
    def generateStartPosition(cls, variantid):
        """Returns the starting position of NQueens based on
        variantID. Follows the same functionality as __init__
        Inputs
            - (Optional) variantid: string

        Outputs
            - A Puzzle of NQueens
        """
        return NQueens(variantid)

    def generateMoves(self, movetype='all'):
        """Generate moves from self (including undos).
        NOTE: For NQueens, all moves are bidirectional, so movetype doens't matter
        Inputs:
            movetype -- str, can be the following
            - 'for': forward moves
            - 'bi': bidirectional moves
            - 'back': back moves
            - 'legal': legal moves (for + bi)
            - 'undo': undo moves (back + bi)
            - 'all': any defined move (for + bi + back)
        Output: Iterable of moves, move must be hashable
        """
        i = 0
        moves = set()
        for p in self.board:
            if p == 0:
                moves.add("A_{}_{}".format('q', i))
            i += 1
        return moves

    def index_to_coordinates(self, i):
        c = str(i // self.size) + str(i % self.size)
        return c

    def coordinates_to_index(self, c):
        col = int(c[:1])
        row = int(c[1:])
        i = col * self.size + row
        return i

    def check_win(self):
        return self.check_col() and self.check_row() and self.check_diag()

    def check_diag(self):
        count = 0
        for k in range(self.size):
            for i, j in zip(range(k, self.size), range(self.size)):
                count += self.board[self.coordinates_to_index(str(i) + str(j))]
            if count >= 2:
                return False
            count = 0
        for k in range(1, self.size):
            for i, j in zip(range(self.size), range(k, self.size)):
                count += self.board[self.coordinates_to_index(str(i) + str(j))]
                if count >= 2:
                    return False
            count = 0
        for k in range(self.size):
            for i, j in zip(range(k, self.size), reversed(range(self.size))):
                count += self.board[self.coordinates_to_index(str(i) + str(j))]
                if count >= 2:
                    return False
            count = 0
        for k in range(1, self.size):
            for i, j in zip(range(self.size), reversed(range(self.size - k))):
                count += self.board[self.coordinates_to_index(str(i) + str(j))]
                if count >= 2:
                    return False
            count = 0
        return True

    def check_row(self):
        for i in range(self.size):
            count = 0
            for j in range(self.size):
                count += self.board[self.coordinates_to_index(str(i) + str(j))]
                if count >= 2:
                    return False
            count = 0
        return True

    def check_col(self):
        for i in range(self.size):
            count = 0
            for j in range(self.size):
                count += self.board[self.coordinates_to_index(str(j) + str(i))]
                if count >= 2:
                    return False
            count = 0
        return True
