"""
File: pegSolitaire.py
Puzzle: Peg Solitaire
Author: Mark Presten (Backend), Cameron Cheung (Backend, AutoGUI)
Date: April 15, 2020
"""

from . import ServerPuzzle
from ..util import *

triangle_maps = [
    [1, 3, 2, 5], # from 0 you can hop over 1 to 3 or over 2 to 5
    [3, 6, 4, 8], # from 1 you can hop over 3 to 6 or over 4 to 8
    [4, 7, 5, 9],
    [1, 0, 4, 5, 6, 10, 7, 12],
    [7, 11, 8, 13],
    [2, 0, 4, 3, 8, 12, 9, 14],
    [3, 1, 7, 8],
    [4, 2, 8, 9],
    [4, 1, 7, 6],
    [5, 2, 8, 7],
    [6, 3, 11, 12],
    [7, 4, 12, 13],
    [7, 3, 8, 5, 11, 10, 13, 14],
    [8, 4, 12, 11],
    [9, 5, 13, 12]
]

star_maps = [
    [2, 5, 3, 7],
    [2, 3, 5, 9],
    [3, 4, 5, 8, 6, 10],
    [2, 1, 6, 9, 7, 11],
    [3, 2, 7, 10],
    [2, 0, 6, 7, 9, 12],
    [],
    [3, 0, 6, 5, 10, 12],
    [5, 2, 9, 10],
    [5, 1, 6, 3, 10, 11],
    [6, 2, 7, 4, 9, 8],
    [7, 3, 10, 9],
    [9, 5, 10, 7]
]

trapezoid_maps = [
    [1,2,4,9,5,11],
    [2,3,5,10,6,12],
    [1,0,6,11,7,13],
    [2,1,7,12,8,14],
    [5,6,9,15,10,17],
    [6,7,10,16,11,18],
    [5,4,7,8,11,17,12,19],
    [6,5,12,18,13,20],
    [7,6,13,19,14,21],
    [4,0,10,11],
    [5,1,11,12],
    [5,0,6,2,10,9,12,13],
    [6,1,7,3,11,10,13,14],
    [7,2,12,11],
    [8,3,13,12],
    [9,4,16,17],
    [10,5,17,18],
    [10,4,11,6,16,15,18,19],
    [11,5,12,7,17,16,19,20],
    [12,6,13,8,18,17,20,21],
    [13,7,19,18],
    [14,8,20,19]
]

# Cross is expected to take 10 hours to solve. Commenting out for now...
#cross_maps = [ [1,2,3,8], [4,9], [1,0,5,10], [4,5,8,15], [9,16], [4,3,10,17], [7,8,13,20], [8,9,14,21], [3,0,7,6,9,10,15,22], [4,1,8,7,10,11,16,23], [5,2,9,8,11,12,17,24], [10,9,18,25], [11,10,19,26], [14,15], [15,16], [8,3,14,13,16,17,22,27], [9,4,15,14,17,18,23,28], [10,5,16,15,18,19,24,29], [17,16], [18,17], [13,6,21,22], [14,7,22,23], [15,8,21,20,23,24,27,30], [16,9,22,21,24,25,28,31], [17,10,23,22,25,26,29,32], [18,11,24,23], [19,12,25,24], [22,15,28,29], [23,16], [24,17,28,27], [27,22,31,32], [28,23], [29,24,31,30] ]

variant_data = {
    'triangle': {'size': 15, 'mps': triangle_maps, 'start': 0b111111111111110, 'slotlabels': 'abcadabcbcadada'},
    'star': {'size': 13, 'mps': star_maps, 'start': 0b1111111111110, 'slotlabels': 'abcbcadacbcba'},
    'trapezoid': {'size': 22, 'mps': trapezoid_maps, 'start': 0b1111111111111111101111, 'slotlabels': 'ababcdcdcabababcdcdcdc'},
    #'cross': {'size': 33, 'mps': cross_maps, 'start': 0b111111111111111101111111111111111, 'slotlabels': 'ababababababababababababababababa'}
}

class Peg(ServerPuzzle):

    id = 'pegsolitaire'
    variants = ["triangle", "star", "trapezoid"]
    #variants = ["triangle", "star", "trapezoid", "cross"]    
    startRandomized = False

    def __init__(self, variant_id, board=None):
        self.variant_id = variant_id
        if board:
            self.board = board
        else:
            self.board = variant_data[variant_id]['start']
        
    @property
    def variant(self):
        return self.variant_id
    
    def __hash__(self):
        return self.board

    def primitive(self, **kwargs):
        # The position is primitive if one bit is set, i.e. self.board
        # is a power of 2. We also check that self.board is nonzero.
        if (self.board & (self.board - 1)) == 0 and self.board:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        src, dest = move
        jump_data = variant_data[self.variant_id]['mps'][src]
        over = jump_data[jump_data.index(dest) - 1]
        return Peg(self.variant_id, self.board ^ (1 << src) ^ (1 << over) ^ (1 << dest))

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = []
        key = False

        if movetype=='all':
            key = True

        size = variant_data[self.variant_id]['size']
        mps = variant_data[self.variant_id]['mps']

        if movetype=='for' or movetype=='legal' or key:
            # if over slot is filled and dest slot is empty then this is a move
            for src in range(size):
                if self.board & (1 << src):
                    for j in range(0, len(mps[src]), 2):
                        over, dest = mps[src][j], mps[src][j + 1]
                        if self.board & (1 << over) and (self.board >> dest) & 1 == 0:
                            moves.append((src, dest))
        if movetype=='undo' or movetype=='back' or key:
            # if over slot is empty and src slot is empty then this is an undomove
            for dest in range(size):
                if self.board & (1 << dest):
                    for j in range(0, len(mps[dest]), 2):
                        over, src = mps[dest][j], mps[dest][j + 1]
                        if (self.board >> over) & 1 == 0 and (self.board >> src) & 1 == 0:
                            moves.append((src, dest))

        return moves

    def generateSolutions(self):
        return [Peg(self.variant_id, 1 << i) for i in range(variant_data[self.variant_id]['size'])]
    
    @classmethod
    def fromHash(cls, variant_id, hash_val):
        puzzle = cls(variant_id)
        puzzle.board = hash_val
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        if not isinstance(variant_id, str): raise TypeError("Invalid variantid")
        if variant_id not in Peg.variants: raise IndexError("Out of bounds variantid")
        return Peg(variant_id)

    @classmethod
    def fromString(cls, variant_id, position_str):
        try:
            board = 0
            for i in range(variant_data[variant_id]['size']):
                if position_str[i] != '-':
                    board |= (1 << i)
            return Peg(variant_id, board)
        except Exception as _:
            raise PuzzleException("Invalid puzzleid")

    def toString(self, mode):
        output = ''
        if mode == StringMode.AUTOGUI:
            output = '1_'
            slotlabels = variant_data[self.variant_id]['slotlabels']
            for i in range(variant_data[self.variant_id]['size']):
                if self.board & (1 << i):
                    output += slotlabels[i]
                else:
                    output += '-'
        else:
            output = ''.join([('x' if self.board & (1 << i) else '-') for i in range(variant_data[self.variant_id]['size'])])
        return output
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return f'M_{move[0]}_{move[1]}_x'
        else:
            return f'{move[0]} → {move[1]}'
    
    @classmethod
    def isLegalPosition(cls, positionid):
        """Checks if the Puzzle is valid given the rules.
        For example, Hanoi cannot have a larger ring on top of a smaller one.
        Outputs:
            - True if Puzzle is valid, else False
        """
        return True
