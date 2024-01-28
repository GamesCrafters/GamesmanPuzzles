"""
File: toadsandfrogspuzzle.py
Puzzle: Toads and Frogs Puzzle
Author: Mark Presten (Backend), Cameron Cheung (AutoGUI)
Date: April 25, 2020
"""

from . import ServerPuzzle
from ..util import *

class ToadsAndFrogsPuzzle(ServerPuzzle):

    id      = 'toadsandfrogspuzzle'
    variants = ["4", "6", "8", "10"] # Number of frogs and toads total, must be even
    startRandomized = False

    def __init__(self, variant_id, **kwargs):
        self.num_frogstoads = int(variant_id)
        self.board = ['x'] * (self.num_frogstoads >> 1) + ['-'] + ['o'] * (self.num_frogstoads >> 1)

    def __str__(self, **kwargs):
        return str(self.board)

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself.
        Example: '5x5', '3x4', 'reverse3x3'
        """
        return str(self.num_frogstoads)

    def primitive(self, **kwargs):
        if self.board == ['o'] * (self.num_frogstoads >> 1) + ['-'] + ['x'] * (self.num_frogstoads >> 1):
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = []
        if movetype=='bi':
            return []
        pad_amount = 2
        padded_board = ['p', 'p'] + self.board[:] + ['p', 'p']
        blank_idx = padded_board.index('-')
        if movetype in ('for', 'legal', 'all'):
            if padded_board[blank_idx - 1] == 'x':
                moves.append(blank_idx - 1 - pad_amount)
            if padded_board[blank_idx + 1] == 'o':
                moves.append(blank_idx + 1 - pad_amount)
            if padded_board[blank_idx - 2] == 'x' and padded_board[blank_idx - 1] == 'o':
                moves.append(blank_idx - 2 - pad_amount)
            if padded_board[blank_idx + 2] == 'o' and padded_board[blank_idx + 1] == 'x':
                moves.append(blank_idx + 2 - pad_amount)
        if movetype in ('undo', 'back', 'all'):
            if padded_board[blank_idx - 1] == 'o':
                moves.append(blank_idx - 1 - pad_amount)
            if padded_board[blank_idx + 1] == 'x':
                moves.append(blank_idx + 1 - pad_amount)
            if padded_board[blank_idx - 2] == 'o' and padded_board[blank_idx - 1] == 'x':
                moves.append(blank_idx - 2 - pad_amount)
            if padded_board[blank_idx + 2] == 'x' and padded_board[blank_idx + 1] == 'o':
                moves.append(blank_idx + 2 - pad_amount)
            
        return moves

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = ToadsAndFrogsPuzzle(str(self.num_frogstoads))
        new_board = self.board[:]
        new_board[new_board.index('-')] = new_board[move]
        new_board[move] = '-'
        newPuzzle.board = new_board
        return newPuzzle

    ### ____________ Solver Funcs ________________

    def __hash__(self):
        h = 0
        copy = self.board[:]
        blank_idx = copy.index('-')
        copy.pop(blank_idx)
        for i in range(self.num_frogstoads):
            if copy[i] == 'x':
                h |= (1 << i)
        return (blank_idx << self.num_frogstoads) | h

    def generateSolutions(self, **kwargs):
        newPuzzle = ToadsAndFrogsPuzzle(str(self.num_frogstoads))
        newPuzzle.board = ['o'] * (self.num_frogstoads >> 1) + ['-'] + ['x'] * (self.num_frogstoads >> 1)
        return [newPuzzle]

    ### ________ Server _________
    @classmethod
    def fromHash(cls, variantid, hash_val):
        puzzle = cls(variantid)
        board = []
        for i in range(puzzle.num_frogstoads):
            if hash_val & (1 << i):
                board.append('x')
            else:
                board.append('o')
        board.insert(hash_val >> puzzle.num_frogstoads, '-')
        return puzzle

    @classmethod
    def fromString(cls, variant_id, positionid):
        """Returns a Puzzle object based on positionid
        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))
        Inputs:
            positionid - String id from puzzle
        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        board = list(positionid.split('_')[-1])
        puzzle = ToadsAndFrogsPuzzle(variant_id)
        puzzle.board = board
        return puzzle
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return f"A_h_{move}_x"
        else:
            return str(move + 1) # 1-index

    def toString(self, mode):
        """Returns a position string
        Outputs:
            String Puzzle
        """
        prefix = '1_' if mode == StringMode.AUTOGUI else ''
        return prefix + ''.join(self.board)

    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        """Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified
        For example, Hanoi cannot have a larger ring on top of a smaller one.
        Outputs:
            - True if Puzzle is valid, else False
        """
        return True

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in ToadsAndFrogsPuzzle.variants: raise IndexError("Out of bounds variantid")
        return ToadsAndFrogsPuzzle(variantid)
