"""
File: spinout.py
Puzzle: Spinout
Author: Joshua Almario, Darren Ting
Date: 2025-03-10
"""
from . import Puzzle
#from . import ServerPuzzle
from ..util import *
from enum import Enum
class Tiles(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT_FLAT = 4
    UP_FLAT = 5
    RIGHT_FLAT = 6
    DOWN_FLAT = 7
class Spinout(Puzzle):

    id = 'spinout'
    startRandomized = False

    # ← → ↑ ↓
    # ⇐ ⇒ ⇑ ⇓
    
    '''Tiles = array of 0-4
        0 = left 
        1 = up
        2 = right
        3 = down '''
    
    '''Hash representation - tuple:
        (track, tile_index)
    '''
    #used for toString()
    tile_dict = {
        Tiles.LEFT : "←",
        Tiles.UP : "↑",
        Tiles.RIGHT : "→",
        Tiles.DOWN : "↓",
        Tiles.LEFT_FLAT : "⇐",
        Tiles.UP_FLAT : "⇑",
        Tiles.RIGHT_FLAT : "⇒",
        Tiles.DOWN_FLAT : "⇓"
    }

    def concaveLeft(tile) -> bool:
        '''If the left side of the tile is concave'''
        match tile:
            case Tiles.LEFT:
                return False
            case Tiles.UP:
                return True
            case Tiles.RIGHT:
                return True
            case Tiles.DOWN:
                return True
            case Tiles.LEFT_FLAT:
                return False
            case Tiles.UP_FLAT:
                return True
            case Tiles.RIGHT_FLAT:
                return False
            case Tiles.DOWN_FLAT:
                return True
            case _: # shouldn't happen
                return ValueError("Invalid tile")
                
    def concaveRight(tile) -> bool:
        '''If the right side of the tile is concave'''
        match tile:
            case Tiles.LEFT:
                return True
            case Tiles.UP:
                return True
            case Tiles.RIGHT:
                return False
            case Tiles.DOWN:
                return True
            case Tiles.LEFT_FLAT:
                return False
            case Tiles.UP_FLAT:
                return True
            case Tiles.RIGHT_FLAT:
                return False
            case Tiles.DOWN_FLAT:
                return True
            case _: # shouldn't happen
                return ValueError("Invalid tile")

    def slidable(tile) -> bool:
        '''If both the top and bottom of the tile are concave'''
        #LEFT, RIGHT, LEFT_FLAT, RIGHT_FLAT can slide
        match tile:
            case Tiles.LEFT:
                return True
            case Tiles.UP:
                return False
            case Tiles.RIGHT:
                return True
            case Tiles.DOWN:
                return False
            case Tiles.LEFT_FLAT:
                return True
            case Tiles.UP_FLAT:
                return False
            case Tiles.RIGHT_FLAT:
                return True
            case Tiles.DOWN_FLAT:
                return False
            case _: # shouldn't happen
                return ValueError("Invalid tile")

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
        self.track = [Tiles.UP] + [Tiles.LEFT] * 5 + [Tiles.LEFT_FLAT]
        self.tile_index = 6
        #self.state = (self.track, self.tile_index)
        
    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    
    def __hash__(self):
        """ Return a hash value of your position """
        return (self.track, self.tile_index)

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        if all(map(self.slidable, self.track)):
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        """
        Return an instance of the puzzle class corresponding to the
        child puzzle position that results from doing the input `move`
        on the current position.
        """

        match move:
            case "cw":
                self.track[self.tile_index] = (self.track[self.tile_index] - 1) % 4
            case "ccw":
                self.track[self.tile_index] = (self.track[self.tile_index] + 1) % 4
            case "left":
                self.tile_index -= 1
            case "right":
                self.tile_index += 1

        return Spinout(self.variant_id, (self.track, self.tile_index))

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        """
        See this link https://github.com/GamesCrafters/GamesmanPuzzles/blob/master/guides/tutorial/02_Moves.md
        to understand what the `movetype` parameter means.
        """
        moves = []
        if self.tile_index > 0 and self.slidable(self.track[self.tile_index - 1]):
            moves.append("left")

        

        '''
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
        '''
        return moves

    def generateSolutions(self):
        """
        Return a list of instances of the puzzle class where each instance
        is a possible "solved" state of the puzzle.
        """
        #only one solvable state
        return [Spinout(self.variant_id, 10)]
    
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
        return Spinout(variant_id, 0)

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
            return Spinout(variant_id, state)
        except Exception as _:
            raise PuzzleException("Invalid puzzleid")

    def toString(self, mode: StringMode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle position -- String
            [{0}, 0, 0, 0, 0, 0, 0, 0]
            tile_index is 0
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE
        if mode == StringMode.AUTOGUI:
            # If the mode is "autogui", return an autogui-formatted position string
            return f'1_{(self.track, self.move_index)}'
        else:
            # Otherwise, return a human-readable position string.
            curr_index = 0
            for tile in self.track:
                
                if curr_index == self.tile_index:
                    track_str += " {" +  str(tile) + "}," 
                else:
                    track_str += " " + str(tile) + "," 
                curr_index += 1
            return "[" + track_str + "]"
        
    
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
            match move:
                case "cw":
                    return str(move)
                case "ccw":
                    return str(move)
                case "left":
                    return str(move)
                case "right":
                    return str(move)
        else:
            # Move is already a string
            return str(move)
    
    @classmethod
    def isLegalPosition(cls, position_str):
        """Checks if the Puzzle is valid given the rules."""
        
        return True
