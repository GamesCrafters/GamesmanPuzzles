"""
File: examplepuzzle.py
Puzzle: Example Puzzle
Author: Firstname Lastname
Date: YYYY-MM-DD
"""

"""
In this example puzzle, the player starts at state 0 and can either
add 1 or 2 to the current state. The puzzle is solved when the player
reaches 10.
There are two variants. In variant1, you can add 0 to the current state
if the current state is 5.
"""

from . import ServerPuzzle
from ..util import *

class ExamplePuzzle(ServerPuzzle):

    id = 'examplepuzzle'
    variants = ["variant0", "variant1"]
    startRandomized = False

    def __init__(self, variant_id: str, state = 0):
        """
        Your constructor can have any signature you'd like,
        because it is only called by the other methods of this class.
        If your puzzle supports multiple variants, it should
        receive some information on the variant as input.

        An instance of the puzzle class represents a position
        in the puzzle, so the constructor should take in information
        that sufficienctly defines a position as input.
        """
        self.variant_id = variant_id
        self.state = state
        
    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    
    def __hash__(self):
        """ Return a hash value of your position """
        return self.state

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        if self.state == 10:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        """
        Return an instance of the puzzle class corresponding to the
        child puzzle position that results from doing the input `move`
        on the current position.
        """
        return ExamplePuzzle(self.variant_id, self.state + move)

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        """
        See this link https://github.com/GamesCrafters/GamesmanPuzzles/blob/master/guides/tutorial/02_Moves.md
        to understand what the `movetype` parameter means.
        """
        moves = []

        if movetype=='for' or movetype=='legal' or movetype=='all':
            if self.state < 8:
                moves += [1, 2]
            elif self.state == 9:
                moves += [1]
            
            if self.variant_id == 'variant1' and self.state == 5:
                moves += [0]
        if movetype=='undo' or movetype=='back' or movetype=='all':
            if self.state > 1:
                moves += [-1, -2]
            elif self.state == 1:
                moves += [-1]
            
            if self.variant_id == 'variant1' and self.state == 5 and 0 not in moves:
                moves += [0]
            
        return moves

    def generateSolutions(self):
        """
        Return a list of instances of the puzzle class where each instance
        is a possible "solved" state of the puzzle.
        """
        return [ExamplePuzzle(self.variant_id, 10)]
    
    @classmethod
    def fromHash(cls, variant_id, hash_val):
        """
        Return an instance of the puzzle class given by the input hash value.
        """
        puzzle = cls(variant_id)
        puzzle.board = hash_val
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        """
        Return an instance of the Puzzle Class corresponding to the initial position.
        """
        return ExamplePuzzle(variant_id, 0)

    @classmethod
    def fromString(cls, variant_id, position_str):
        """ Given an input human-readable puzzle position string, 
        return an instance of the Puzzle Class corresponding to that position.

        Inputs:
            position_str - Human-readable string representation of the puzzle, as given
               by self.toString(StringMode.HUMAN_READABLE)

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        try:
            state = int(position_str)
            return ExamplePuzzle(variant_id, state)
        except Exception as _:
            raise PuzzleException("Invalid puzzleid")

    def toString(self, mode: StringMode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle position -- String
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE
        if mode == StringMode.AUTOGUI:
            # If the mode is "autogui", return an autogui-formatted position string
            return f'1_{self.state}'
        else:
            # Otherwise, return a human-readable position string.
            return str(self.state)
        
    
    def moveString(self, move, mode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the move -- String
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE
        if mode == StringMode.AUTOGUI:
            # If the mode is "autogui", return an autogui-formatted move string
            if move == 0:
                return f'A_-_{self.state}_x'
            return f'M_{self.state}_{self.state + move}_x'
        else:
            # Otherwise, return a human-readable move string.
            return str(move)
    
    @classmethod
    def isLegalPosition(cls, position_str):
        """Checks if the Puzzle is valid given the rules."""
        state = int(position_str)
        return 0 <= state <= 10 
