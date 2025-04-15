"""
File: spinout.py
Puzzle: Spinout
Author: Joshua Almario, Darren Ting
Date: 2025-03-10
"""
#from . import ServerPuzzle
#from ..util import *
#from solvers import GeneralSolver
#from players import TUI
from enum import Enum
from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI
import hashlib

class Tiles(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT_FLAT = 4
    UP_FLAT = 5
    RIGHT_FLAT = 6
    DOWN_FLAT = 7

# ugly set of helper methods ever don't kill us lol
def concaveLeft(tile) -> bool:
    '''If the left side of the tile is concave'''
    if tile.value < 0 or tile.value > 7:
        return ValueError("Invalid tile")
    return tile != Tiles.LEFT and tile != Tiles.LEFT_FLAT and tile != Tiles.RIGHT_FLAT
            
def concaveRight(tile) -> bool:
    '''If the right side of the tile is concave'''
    if tile.value < 0 or tile.value > 7:
        return ValueError("Invalid tile")
    return tile != Tiles.RIGHT and tile != Tiles.LEFT_FLAT and tile != Tiles.RIGHT_FLAT

def slidable(tile) -> bool:
    '''If both the top and bottom of the tile are concave'''
    #LEFT, RIGHT, LEFT_FLAT, RIGHT_FLAT can slide
    if tile.value < 0 or tile.value > 7:
        return ValueError("Invalid tile")
    return tile.value % 2 == 0

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

alphabet_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#used for toString()

total_positions = 12

reversed_tile_dict = {tile_dict[key] : key for key in tile_dict.keys()}

class Spinout(ServerPuzzle):
    id = 'spinout'
    variants = ["5_piece"]
    startRandomized = False

    '''Hash representation - tuple:
        (track, tile_index)
    '''

    def __init__(self, variant_id: str = None, state = None):
        """
        Your constructor can have any signature you'd like,
        because it is only called by the other methods of this class.
        If your puzzle supports multiple variants, it should
        receive some information on the variant as input.

        An instance of the puzzle class represents a position
        in the puzzle, so the constructor should take in information
        that sufficienctly defines a position as input.
        """
        #initial state: [Tiles.UP] + [Tiles.LEFT] * 5 + [Tiles.LEFT_FLAT]
        #Number of Tiles.LEFT has been temporarily reduced due to remoteness byte overflow issues

        self.variant_id = variant_id
        if state == None:
            self.track = [Tiles.UP] + [Tiles.LEFT] * 3 + [Tiles.LEFT_FLAT]
            self.tile_index = len(self.track) - 1
        else:
            self.track = deepcopy(state[0])
            self.tile_index = state[1]
        
    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    
    def __hash__(self):
        """ Return a hash value of your position """
        cool_string = \
            (str
                (list
                    (map
                        (lambda x : x.value, self.track)
                    )
                )
            ) + \
            str(self.tile_index)
        result = hashlib.sha256(cool_string.encode())
        result_bytes = result.digest()
        result_int = int.from_bytes(result_bytes, byteorder="big") % 200000000
        # print(result, self.track, self.tile_index)
        #print(result, cool_string, self.toString(StringMode.HUMAN_READABLE))
        return result_int

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        # print(self.toString(StringMode.HUMAN_READABLE))
        if all(map(slidable, self.track)):
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        """
        Return an instance of the puzzle class corresponding to the
        child puzzle position that results from doing the input `move`
        on the current position.
        """

        # Important note, move "left" is moving the slider right, same with the inverse for "right"
        # Essentially, one is moving to the piece on the left or right, not moving the entire board left or right

        # match move:
        #     case "cw":
        #         if self.track[self.tile_index] > 3:
        #             self.track[self.tile_index] = (self.track[self.tile_index] - 1) % 4 + 4
        #         else:
        #             self.track[self.tile_index] = (self.track[self.tile_index] - 1) % 4
        #     case "ccw":
        #         if self.track[self.tile_index] > 3:
        #             self.track[self.tile_index] = (self.track[self.tile_index] - 1) % 4 + 4
        #         else:
        #             self.track[self.tile_index] = (self.track[self.tile_index] + 1) % 4
        #     case "left":
        #         self.tile_index -= 1
        #     case "right":
        #         self.tile_index += 1
        s = Spinout(self.variant_id, (self.track, self.tile_index))

        if move == "cw":
            if self.track[self.tile_index].value > 3:
                s.track[self.tile_index] = Tiles((self.track[self.tile_index].value + 1) % 4 + 4)
            else:
                s.track[self.tile_index] = Tiles((self.track[self.tile_index].value + 1) % 4)
        elif move == "ccw":
            if self.track[self.tile_index].value > 3:
                s.track[self.tile_index] = Tiles((self.track[self.tile_index].value - 1) % 4 + 4)
            else:
                s.track[self.tile_index] = Tiles((self.track[self.tile_index].value - 1) % 4)
        else:
            split_move = move.split("_")
            if len(split_move) == 2:
                if split_move[0] == "left":
                    s.tile_index -= int(split_move[1])
                if split_move[0] == "right":
                    s.tile_index += int(split_move[1])
            else:
                raise ValueError("Incorrect move format")

        return s

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        """
        See this link https://github.com/GamesCrafters/GamesmanPuzzles/blob/master/guides/tutorial/02_Moves.md
        to understand what the `movetype` parameter means.
        """
        moves = []
        current_tile = self.track[self.tile_index]
        if ((self.tile_index == len(self.track) - 1 or concaveLeft(self.track[self.tile_index + 1])) and
            (self.tile_index == 0 or concaveRight(self.track[self.tile_index - 1]))):
            moves.append("cw")
            moves.append("ccw")
        if not (current_tile == Tiles.DOWN or current_tile == Tiles.DOWN_FLAT):
            i = 0
            while (self.tile_index - i > 0 and
                # Last tile or if tile to the right is slidable
                (self.tile_index - i >= len(self.track) - 1 or slidable(self.track[self.tile_index - i + 1]))):
                moves.append(f"left_{i + 1}")
                i += 1
                # Not last tile
            i = 1
            while (self.tile_index + i < len(self.track)):
                moves.append(f"right_{i}")
                i += 1

        # Important note, move "left" is moving the slider right, same with the inverse for "right"
        # Essentially, one is moving to the piece on the left or right, not moving the entire board left or right
        return moves

    def generateSolutions(self):
        """
        Return a list of instances of the puzzle class where each instance
        is a possible "solved" state of the puzzle.
        """
        #only one solvable state, assumes that every state of the puzzle can reach this state
        return [Spinout(self.variant_id, ([Tiles.LEFT] * 4 + [Tiles.LEFT_FLAT], i) ) for i in range(5)] + \
            [Spinout(self.variant_id, ([Tiles.LEFT] * 4 + [Tiles.RIGHT_FLAT], i) ) for i in range(5)] 
    
    @classmethod
    def fromHash(cls, variant_id, hash_val):
        """
        Return an instance of the puzzle class given by the input hash value.
        """
        #assuming that this is outdated
        puzzle = cls(variant_id)
        puzzle.track = list(hash_val[0])
        puzzle.tile_index = hash_val[1]
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id = None, **kwargs):
        """
        Return an instance of the Puzzle Class corresponding to the initial position.
        """
        return Spinout(variant_id)

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
            no_parens = position_str.replace("(", "").replace(")","")
            result = []
            for char in no_parens:
                result.append(reversed_tile_dict[char])
            tile_index = position_str.find("(")

            
            return Spinout(variant_id, (result, tile_index))
        except Exception as _:
            raise PuzzleException("Invalid puzzleid")

    def toString(self, mode: StringMode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle position -- String
            (←)←←←←←←←
            tile_index is 0
        """
        if mode == StringMode.AUTOGUI:
            # If the mode is "autogui", return an autogui-formatted position string
            result = "1_"
            for left_empty_pos in range(3 + (4 - self.tile_index)):
                result += "-"
                
            #first 4 tiles
            for index in range(len(self.track) - 1):
                result += alphabet_string[self.track[index].value + index * 4]
            #last tile
            result += alphabet_string[self.track[4].value + 3 * 4]

            for right_empty_pos in range(self.tile_index):
                result += "-"

            return result
        else:
            # Otherwise, return a human-readable position string.
            curr_index = 0
            track_str = ""
            for tile in self.track:
                if curr_index == self.tile_index:
                    track_str += "(" +  str(tile_dict[tile]) + ")" 
                else:
                    track_str += str(tile_dict[tile])
                curr_index += 1
            return track_str
        # else:
        #     #human readable
        #     return str([{self.tile_index}] + self.track)

        
    
    def moveString(self, move, mode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the move -- String
        """
        #center 7 (index 6) is the piece that can be rotated
        if mode == StringMode.AUTOGUI:
            split_move = move.split("_")
            if len(split_move) == 2:
                #slide
                if split_move[0] == "left":
                    return f"M_{7 - int(split_move[1])}_{7}_s"
                else:
                    return f"M_{7 + int(split_move[1])}_{7}_s"
            else:
                #rotating
                if move == "cw":
                    return f"A_c_{13}_r"
                else:
                    return f"A_w_{14}_r"
        else:
            return str(move)
    
    @classmethod
    def isLegalPosition(cls, position_str):
        """Checks if the Puzzle is valid given the rules."""
        
        puzzle = cls.fromString(position_str)

        i = 0
        for tile in puzzle.track:
            if i != puzzle.tile_index and (tile == Tiles.DOWN or tile == Tiles.DOWN_FLAT):
                raise PuzzleException("Only current tile can face down!")
            if (i < len(puzzle.track) and not concaveRight(tile) and not concaveLeft(puzzle.track[i + 1])):
                raise PuzzleException("Two convex sides facing each other!")
            i += 1
        if not all(map(slidable, puzzle.track[puzzle.tile_index + 1:])):
            raise PuzzleException("All tiles after current must face sideways!")
        
        return True

p = Spinout()
TUI(p, GeneralSolver(p), info=True)
