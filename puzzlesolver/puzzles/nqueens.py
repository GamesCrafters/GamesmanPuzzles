"""
File: nqueens.py
Puzzle: N Queens Puzzle
Author: Mia Campdera-Pulido, Cameron Cheung
Date: March 17, 2021
"""

"""N Queens Puzzle
 https://en.wikipedia.org/wiki/Eight_queens_puzzle
"""
from . import ServerPuzzle
from ..util import *
import math
import itertools

class NQueens(ServerPuzzle):

    id = 'nqueens'

    variants = [str(N) for N in range(4, 10)]
    startRandomized = False

    def __init__(self, variant_id, bitboard = 0, placed_so_far = 0):
        self.variant_id = variant_id
        self.N = int(variant_id)
        self.bitboard = bitboard
        self.placed_so_far = placed_so_far
        
    @property
    def variant(self):
        return str(self.N)
    
    def safe_squares(self, bitboard):
        """
        A "safe square" is a square that's not attacked by any of the queens on the
        board. A queen does not attack its own square, but another queen might attack it.
        Return a bitstring where the i-th bit indicates whether the square is
        safe (1) or attacked (0).
        """

        N2 = self.N * self.N
        attacked_bitstring = 0
        for b in range(N2):
            if bitboard & (1 << b):
                l = b - (b % self.N)
                for i in range(l, l + self.N): # Mark row as attacked
                    if i != b:
                        attacked_bitstring |= (1 << i)
                for i in range(b % self.N, N2, self.N): # Mark column as attacked
                    if i != b:
                        attacked_bitstring |= (1 << i)
                
                i = b + self.N + 1 # Down right
                while i % self.N != 0 and i < N2:
                    attacked_bitstring |= (1 << i)
                    i += self.N + 1

                i = b + self.N - 1 # Down left
                while i % self.N != self.N - 1 and i < N2:
                    attacked_bitstring |= (1 << i)
                    i += self.N - 1

                i = b - (self.N + 1) # Up left
                while i >= 0 and i % self.N != self.N - 1:
                    attacked_bitstring |= (1 << i)
                    i -= (self.N + 1)

                i = b - (self.N - 1) # Up right
                while i >= 0 and i % self.N != 0:
                    attacked_bitstring |= (1 << i)
                    i -= (self.N - 1)
        
        return ((1 << (self.N * self.N)) - 1) ^ attacked_bitstring
    
    def nonattacking_configuration(self, bitboard, safe_squares):
        """
        Check whether n (which is some number between 0 and N inclusive) queens
        on the board are in a non-attacking configuration given the safe squares
        bitstring of the bitboard baord.
        Does not indicate whether the current board will lead to a completed puzzle,
        only checks whether the queens placed thus far don't attack each other.
        Return True if non-attacking, False otherwise.
        """
        return safe_squares | bitboard == safe_squares


    def F(N, r):
        return math.factorial(N) // math.factorial(N - r)

    def G(N, placed_so_far):
        return math.comb(N, placed_so_far) * NQueens.F(N, placed_so_far)

    def B(N, placed_so_far):
        """
            Calculate bias given number of queens placed so far.
        """
        total = 0
        for i in range(placed_so_far):
            total += NQueens.G(N, i)
        return total
    
    def inv_B(N, hash_val):
        """
            Given hash value of a position, return number of queens placed so far
            and hash value with num-queens-placed bias subtracted away.
        """
        placed_so_far = 0
        while True:
            g = NQueens.G(N, placed_so_far)
            if hash_val - g < 0:
                return placed_so_far, hash_val
            hash_val -= g
            placed_so_far += 1
    
    def h1(N, row_ids):
        """
            Given occupied rows in ascending order.
        """
        h1 = 0
        placed_so_far = len(row_ids)
        m = 0
        for i in range(placed_so_far):
            for sw in range(m, row_ids[i]):
                h1 += math.comb(N - 1 - sw, placed_so_far - i - 1)
            m = row_ids[i] + 1
        return h1
    
    def inv_h1(N, placed_so_far, h1):
        row_ids = []
        total, m, q = 0, 0, 0
        for i in range(placed_so_far):
            for sw in range(m, N):
                q = math.comb(N - 1 - sw, placed_so_far - i - 1)
                if total + q > h1:
                    row_ids.append(sw)
                    m = sw + 1
                    break
                total += q
        return row_ids

    def h2(N, col_ids):
        """
            Given the columns of the queens, ordered according to 
            ascending order of rows, calculate the h2 part of the calculation.
        """
        h2, r = 0, 0
        empty_cols = list(range(N))
        for col_id in col_ids:
            normalized_col_id = empty_cols.index(col_id)
            h2 += normalized_col_id * NQueens.F(N, r)
            empty_cols.remove(col_id)
            r += 1
        return h2

    def inv_h2(N, placed_so_far, h2):
        normalized_col_ids = []
        for r in range(N, N - placed_so_far, -1):
            normalized_col_ids.append(h2 % r)
            h2 //= r
        empty_cols = list(range(N))
        col_ids = []
        for normalized_col_id in normalized_col_ids:
            col_ids.append(empty_cols[normalized_col_id])
            empty_cols.pop(normalized_col_id)
        return col_ids     

    def __hash__(self):
        # Count how many queens placed so far, calculate big bias
        # Get sorted ids of rows containing a queen, calculate h1
        # Get cols of each queen in the containing columns, calculate h2
        placed_so_far = 0
        row_ids = [] # row ids will be in sorted order
        col_ids = []
        for b in range(self.N * self.N):
            if self.bitboard & (1 << b):
                placed_so_far += 1
                row_ids.append(b // self.N)
                col_ids.append(b % self.N)
        B = NQueens.B(self.N, placed_so_far)
        h1 = NQueens.h1(self.N, row_ids)
        h2 = NQueens.h2(self.N, col_ids)
        return B + h1 * NQueens.F(self.N, placed_so_far) + h2

    def primitive(self, **kwargs):
        if self.placed_so_far == self.N:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        bitboard, placed_so_far = self.bitboard, self.placed_so_far
        if bitboard & (1 << move): # is an undomove
            placed_so_far -= 1
        else: # is a forward move
            placed_so_far += 1
        bitboard ^= (1 << move)
        return NQueens(self.variant_id, bitboard, placed_so_far)

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = []
        if movetype in ('for', 'legal', 'all'):
            # The squares where you can place another queen such that it doesn't attack / is not
            # attacked by any other queens are the safe squares [see definition in safe_squares()]
            # excluding safe squares that have queens already on them. We can assume self.bitboard is a 
            # noonattacking configuration [see definition in nonattacking_configuration()] to begin with.
            legal_placements = self.safe_squares(self.bitboard) ^ self.bitboard
            moves.extend([b for b in range(self.N * self.N) if legal_placements & (1 << b)]) # strings
        if movetype in ('undo', 'back', 'all'):
            moves.extend([b for b in range(self.N * self.N) if self.bitboard & (1 << b)]) # ints
        return moves

    def generateSolutions(self):
        solutions = []
        for perm in itertools.permutations(range(self.N)):
            bitboard = 0
            for i in range(self.N):
                bitboard |= (1 << (self.N * i + perm[i]))
            if self.nonattacking_configuration(bitboard, self.safe_squares(bitboard)):
                solutions.append(NQueens(self.variant_id, bitboard, self.N))
        return solutions
    
    @classmethod
    def fromHash(cls, variant_id, hash_val):
        puzzle = cls(variant_id)
        # count how many queens on board, calculate big bias and subtract it away
        # get sorted ids of rows containing a queen, calculate h1
        # get cols of each queen in the containing columns, assemble board

        placed_so_far, hash_val = NQueens.inv_B(puzzle.N, hash_val)

        m = NQueens.F(puzzle.N, placed_so_far)
        row_ids = NQueens.inv_h1(puzzle.N, placed_so_far, hash_val // m)
        col_ids = NQueens.inv_h2(puzzle.N, placed_so_far, hash_val % m)

        for row, col in zip(row_ids, col_ids):
            puzzle.bitboard |= (1 << (row * puzzle.N) + col)
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        return NQueens(variant_id, 0, 0) # Empty Board bitboard = 0

    @classmethod
    def fromString(cls, variant_id, position_str):
        try:
            bitboard, placed_so_far = 0, 0
            for b in range(len(position_str)):
                if position_str[b] == 'Q':
                    bitboard |= (1 << b)
                    placed_so_far += 1
            return NQueens(variant_id, bitboard, placed_so_far)
        except Exception as _:
            raise PuzzleException('Invalid puzzleid')

    def toString(self, mode):
        prefix = '1_' if mode == StringMode.AUTOGUI else ''
        return prefix + ''.join(['Q' if (self.bitboard & (1 << b)) else '-' for b in range(self.N * self.N)])
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return f'A_h_{move}_x'
        else:
            return f"{chr(ord('a') + move % self.N)}{self.N - move // self.N}"