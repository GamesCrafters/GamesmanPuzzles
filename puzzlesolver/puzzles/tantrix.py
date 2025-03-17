"""
File: tantrix.py
Puzzle: Tantrix
Author: Abraham Hsu, Grant Zhao, Aditiya Tummala
Date: 2025-03-16
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *

class Tantrix(ServerPuzzle):

    id = 'tantrix'
    
    # variants defined as number of pieces, sharp, soft, and straight
    variants = ["3|0|0"]

    """
    coord_change defined as follows:
        (0, -2)  : Up
        (1, -1)  : Top Right
        (1, 1)   : Bottom Right
        (0, 2)   : Down
        (-1, 1)  : Bottom Left
        (-1, -1) : Top Left
    
    Puzzle design defined as follows:
        0: Start position of the line
        1: Sharp turn < to the top right
        2: Soft turn ( to the bottom right
        3: Straight | to the bottom
        4: Soft turn ) to the bottom left
        5: Sharp turn > to the top left
    """
    coord_change = [(0,-2), (1, -1), (1, 1), (0, 2), (-1, 1), (-1, -1)]

    def __init__(self, variant_id: str, state = [], pieces = [3, 0, 0]):
        """
            Tantrix class will keep a current index tuple (self.curr_index), which maps to coord_change.
            Current index entries will be in mod 6.
            Sharp, soft, and straight lines/curves will define a change in current index, corresponding to board coordinate changes. 
            The first value is the 'head' and the second value is the 'tail' of the path.

            Tantrix class will also keep a current coordinate (self.curr_coord).
            This will be the physical coordinate of the piece on the implicit graph.

            The path will be saved counter-clockwise in self.state
        """
        self.variant_id = variant_id
        self.state = state # Each element in the state is a description of a puzzle piece (coordinate, design) 
                           # Example (0, 0, 1, 4): puzzle is at coordinate (0,0) and has a soft turn to the bottom left from top right

        self.num_pieces = sum(pieces)
        self.pieces = pieces # [sharp, soft, straight] number of pieces for each

    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    
    def __hash__(self):
        """ Return a hash value of your position """
        hash = "0"
        for state in self.state:
            hash += state[-1]
        return int(hash)

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        front_piece = self.state[0] #Takes the very last piece entered into the puzzle from the front
        back_piece = self.state[-1] #Takes the very last piece entered into the puzzle from the back
        change = self.coord_change[back_piece[3]] #Gets the change in coordinates for the back piece
        new_coordx = back_piece[0] + change[0] #Change the coordinates of the last piece
        new_coordy = back_piece[1] + change[1]
        #Check if the new coordinates equal to the front piece and the length of the puzzle is correct
        if ((new_coordx, new_coordy) == (front_piece[0], front_piece[1])) and (len(self.state) == self.num_pieces):
           return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        """
        Return an instance of the puzzle class corresponding to the
        child puzzle position that results from doing the input `move`
        on the current position.
        """
        pos = move[0] # pos will be 0 or -1 (head or tail)

        if self.state == []:
            prev = 0 #starting edge
            new_coord = (0, 0) #starting position for first piece
        else:
            prev_state = self.state[pos] #Get the previous piece based on head or tail
            prev_curve = (prev_state[2], prev_state[3]) #
            prev = (prev_curve[pos] + 3) % 6
            change = Tantrix.coord_change[prev_curve[pos]]
            new_coord = (prev_state[0] + change[0], prev_state[1] + change[1])

        curve = (move[1] - prev + 6) % 6
        if curve == 1 or curve == 5:
            sharp = self.pieces[0] - 1
        elif curve == 3:
            straight = self.pieces[2] - 1
        else:
            soft = self.pieces[1] - 1
    
        if pos == -1:
            return Tantrix(self.variant_id, deepcopy(self.state).insert(len(self.state), (new_coord[0], new_coord[1], prev, move[1])), [sharp, soft, straight])
        else:
            return Tantrix(self.variant_id, deepcopy(self.state).insert(pos, (new_coord[0], new_coord[1], move[1], prev)), [sharp, soft, straight])

    # Returns the coordinates of each existing piece
    def pieceCoords(self):
        return set([(p[0], p[1]) for p in self.state])
    
    #Returns true if connected piece connects the line
    def pieceConnect(self, xcoord, ycoord, exit):
        for p in self.state:
            if p[0] == xcoord and p[1] == ycoord and p[3] == exit:
                return True
        return False

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        """
        See this link https://github.com/GamesCrafters/GamesmanPuzzles/blob/master/guides/tutorial/02_Moves.md
        to understand what the `movetype` parameter means.
        """
        moves = [] #each element (head or tail of the stack self.state, number 1-5 )
        if self.state == []:
            return [(-1, i) for i in range(1, 6)]
        
        if movetype=='for' or movetype=='legal' or movetype=='all':
            for i in range(-1, 1):
                curr = self.state[i]
                prev_curve = (curr[2], curr[3])
                
                for curve in range(1, 4):
                    if self.pieces[curve - 1] == 0:
                        continue
                    

            pass
        if movetype=='undo' or movetype=='back' or movetype=='all': # backwards.
            pass
            
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
        v = variant_id.split("|")
        pieces = [int(i) for i in v]
        return Tantrix(variant_id, pieces = pieces)

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
