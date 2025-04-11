"""
File: squirrelsgonuts.py
Puzzle: Squirrels Go Nuts
Author: 
Date:
"""


from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.solvers import NoUndoSolver
from puzzlesolver.players import TUI

from ..util import *
from ..puzzles import ServerPuzzle
import random
import os
dirname = os.path.dirname(__file__)

# same as rush hour -> just changes by not exiting
# we want to just check it for when there is no more nuts in the puzzle
# if nut_position == hole_position -> deposit
# if nut_count == 0 -> terminate
class Squirrels(ServerPuzzle):
    id = "squirrels"
    variants = ['starter']
    # "True" would mean that the game would start at a random solvable board,
    # by looking at all solvable hashes -- hence False to ensure we fix a start position
    startRandomized = False

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """
        Return an instance of the Puzzle Class corresponding to the initial position.
        """
        if not isinstance(variantid, str) or variantid not in Squirrels.variants:
            raise TypeError("Invalid variantid")
        return Squirrels(variant_id=variantid)

    def __init__(self, variant_id, puzzle_id=None, pos=None, squirrels_list=None, nuts_list=None, nuts_left=None, hole_list=None, actual_hole_list=None, hole_matching=None):
        """
        Your constructor can have any signature you'd like,
        because it is only called by the other methods of this class.
        If your puzzle supports multiple variants, it should
        receive some information on the variant as input.

        An instance of the puzzle class represents a position
        in the puzzle, so the constructor should take in information
        that sufficienctly defines a position as input.
        """
        super().__init__()
        self.variant_id = variant_id
        self.squirrels_list = squirrels_list
        self.nuts_list = nuts_list
        self.nuts_left = nuts_left
        self.hole_list = hole_list
        self.actual_hole_list = actual_hole_list
        self.pos = pos
        self.hole_coords = [2, 4, 9, 15] # the coordinates in holes
        self.hole_matching = hole_matching # the coordinate to hole piece string matching
        if self.pos is None:
            #/Users/User/Desktop/SquirrelsGoNuts/assets/squirrelsgonuts/starter
            #assets/squirrelsgonuts/starter
            variant_file = f"{dirname}/../assets/squirrelsgonuts/{variant_id}.txt"
            if puzzle_id is None:
                # Search the database for a random puzzle with the given difficulty level.
                #variant_ranges = {"basic": 4943, "medium": 5000, "hard": 4043}
                #puzzle_id = random.randrange(variant_ranges[variant_id])
                puzzle_id = 0
                with open(variant_file, 'r') as variants:
                    for i, variant in enumerate(variants):
                        if i == puzzle_id:
                            self.pos = variant[:].rstrip().split(",")  # remove trailing newline
                            break
        else:
            self.pos = list(self.pos)
        if self.squirrels_list == None and self.nuts_list == None and self.hole_list == None and self.actual_hole_list == None:
            self.squirrels_list = {}
            self.nuts_list = {}
            self.nuts_left = []
            self.hole_list = {}
            self.actual_hole_list = {}
            self.hole_matching = {}
            #print("check")
            for i, piece in enumerate(self.pos):
                if len(piece) == 5: # means we have a hole
                    type, type_index, relation = piece.split("_")
                    if type == "H":
                        self.hole_list[type_index] = relation
                        self.hole_matching[i] = piece
                if len(piece) >= 7: # means this is a nut piece
                    type, type_index, relation, orientation = piece.split("_")
                    if type == "N":
                        if relation == "O":
                            #print(piece)
                            self.nuts_left.append(piece)
                            self.nuts_list[type_index] = piece
                        if type_index not in self.squirrels_list:
                            self.squirrels_list[type_index] = []
                        self.squirrels_list[type_index].append(piece)
        else:
            self.nuts_left = list(self.nuts_left)
            temp = {}
            for tuple_item in self.squirrels_list:
                temp[tuple_item[0]] = list(tuple_item[1])
            self.squirrels_list = temp
            self.nuts_list = dict((x, y) for x, y in self.nuts_list)
            self.hole_list = dict((x, y) for x, y in self.hole_list)
            self.actual_hole_list = dict((x, y) for x, y in self.actual_hole_list)
            self.hole_matching = dict((x, y) for x, y in self.hole_matching)
    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id

    def __hash__(self):
        """ Return a hash value of your position 
        SQUIRRELS GO NUTS:

        - We could hash the position of the squirrels b/c not just a red piece
        - a bit more interesting b/c some squirrels are L shaped
        - 
        
        def __hash__(self):
        Return a hash value of your position 
        SQUIRRELS GO NUTS:

        - We could hash the position of the squirrels b/c not just a red piece
        - a bit more interesting b/c some squirrels are L shaped
        - 
        """
        return hash((
        tuple(self.pos), 
        tuple(sorted(self.hole_matching.items())), 
        tuple(sorted(tuple(self.nuts_left))),  # Ensure nuts_left is a tuple
        tuple(sorted((k, tuple(v)) for k, v in self.squirrels_list.items())),  # Convert nested lists to tuples
        tuple(sorted(self.hole_list.items())),  # Ensure hole_list is included if needed
        tuple(sorted(self.actual_hole_list.items()))  # Ensure actual_hole_list is included
    ))
        #return hash(tuple(self.pos)) # CHECK THIS - USE THIS FOR HASH MAYBE?

    def toString(self, mode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle position -- String
        """
        display = ""
        for i in range(4):
            # modify orienation character so it is instead a string showing if it is up, down, left, right, or otherwise for AUTOGUI
            piece = self.pos[4 * i:4 * (i + 1)]
            # change hole piece if it is filled -> lighter shade for the hole if filled
            if len(piece) == 7:
                return None
            display += str(self.pos[4 * i:4 * (i + 1)]) + "\n" # gets each piece of the first 4 elements then indents
        return display
        

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        if len(self.nuts_left) == 0:
            return PuzzleValue.SOLVABLE
        elif len(self.actual_hole_list) > 0:
            for index, nut_piece in self.actual_hole_list.items():
                # if the nut index is not equal to the hole's nut relation, it's unsolvable
                type, type_index = nut_piece.split("_")
                _, hole_index, nut_relation = self.hole_matching[index].split("_")
                if type_index != nut_relation:
                    return PuzzleValue.UNSOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype="all"):
        if movetype == 'for' or movetype == 'back':
            return tuple()  # All moves are bidirectional
        moves = []
        checked_squirrel = tuple()
        for i, piece in enumerate(self.pos):
            # Check for leftward moves
            if piece in self.nuts_list.values(): # checks if its a squirrel + nut -> can enumerate from there with squirrel index
                type, type_index, relation, orientation = piece.split("_")
                if type_index not in checked_squirrel:
                    num_blocks = len(self.squirrels_list[type_index])
                    # will need to check if the move is also a hole -> can move into holes as well as a move
                    j = 0
                    blocked = False
                    while (i - j) % 4 > 0 and not blocked: # checks if leftward move possible
                        count = []
                        for squirrel_block in self.squirrels_list[type_index]:
                            Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                            Sorientation = int(Sorientation)
                            if (i - j + Sorientation) % 4 > 0:
                                left_block = self.pos[i - j + Sorientation - 1]
                                # if hole or empty or part of this squirrel, we can move
                                if len(left_block) == 5 or left_block == '-' or left_block in self.squirrels_list[type_index]: 
                                    count.append(f"M_{i + Sorientation}_{i - j + Sorientation - 1}_{squirrel_block}") # Move, curr, next, nut index
                                else : blocked = True # can't execute any move past this
                                
                        if len(count) == num_blocks: # if all blocks can move for the squirrel
                            moves.append(count)
                        j += 1
                    j = 0
                    blocked = False
                    while (i + j) % 4 < 3 and not blocked:
                        count = []
                        for squirrel_block in self.squirrels_list[type_index]:
                        # Check for rightward moves
                            Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                            Sorientation = int(Sorientation)
                            if (i + Sorientation + j) % 4 < 3:
                                right_block = self.pos[i + j + 1 + Sorientation]
                                if len(right_block) == 5 or right_block == "-" or right_block in self.squirrels_list[type_index]:
                                    count.append(f"M_{i + Sorientation}_{i + j + 1 + Sorientation}_{squirrel_block}") # CHECK HERE COULD BE SUS
                                else : blocked = True # can't execute any move past this
                        if len(count) == num_blocks:
                            moves.append(count)
                        j += 1
                    j = 1
                    blocked = False
                    while i - 4 * j >= 0 and not blocked:
                        count = []
                        for squirrel_block in self.squirrels_list[type_index]:
                        # Check for upward moves
                            Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                            Sorientation = int(Sorientation)
                            if (i+Sorientation) - 4 * j >= 0:
                                up_block = self.pos[(i + Sorientation) - 4 * j]
                                if len(up_block) == 5  or up_block == "-" or up_block in self.squirrels_list[type_index]:
                                    count.append(f"M_{i + Sorientation}_{(i + Sorientation) - 4 * j}_{squirrel_block}")
                                else : blocked = True # can't execute any move past this
                        if len(count) == num_blocks:
                            moves.append(count)   
                        j += 1
                    j = 1
                    blocked = False
                    while i + 4 * j < 16 and not blocked:
                        count = []
                        for squirrel_block in self.squirrels_list[type_index]:
                        # Check for downward moves
                            Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                            Sorientation = int(Sorientation)
                            if (i + Sorientation) + 4 * j < 16:
                                down_block = self.pos[(i + Sorientation) + 4 * j]
                                if len(down_block) == 5 or down_block == "-" or down_block in self.squirrels_list[type_index]:
                                    count.append(f"M_{i + Sorientation}_{(i + Sorientation) + 4 * j}_{squirrel_block}")
                                else : blocked = True # can't execute any move past this
                        if len(count) == num_blocks:
                            #print(count)
                            moves.append(count)
                        j += 1
                    checked_squirrel = checked_squirrel + tuple(type_index)
        returner = tuple()
        for piece in moves:
            returner = returner + (tuple(piece),)
        return tuple(returner)
        

    def doMove(self, move, **kwargs):
        new_pos = list(self.pos.copy())
        new_nuts_left = self.nuts_left.copy()
        new_actual_hole_list = self.actual_hole_list.copy()
        for piece in move:
            #print(piece)
            _, start, end, type, type_index, relation, orientation = piece.split("_")
            start = int(start)
            end = int(end)
            # Make sure to adjust when a nut is in a hole
            # First check the move's orientation to know which way to move
            # check if new piece has hole -> means it needs to be updated into the hole placements
            piece_string = type+"_"+type_index+"_"+relation+"_"+orientation
            new_pos[end] = piece_string
            if end in self.hole_coords and self.nuts_list[type_index] in self.nuts_left and relation == "O": 
                # CHECK THIS UPDATE: now checks if hole and if still usable hole for nuts -> past code (self.pos[end] in self.hole_matching.values())
                # WAIT should check if the hole is already filled??
                new_actual_hole_list[end] = type + "_" + type_index # hole location : nut index
                new_nuts_left.remove(self.nuts_list[type_index]) # takes the nuts on the board off -> no more nut to consider
            if start not in self.hole_coords and not (len(new_pos[start]) == 7 and new_pos[start] != piece_string): # needs to check that it is not a nut
                new_pos[start] = "-"
            if start in self.hole_coords: # if there was a hole here
                new_pos[start] = self.hole_matching[start] # initialize back to the previous hole
                # check if the old piece has a hole inside, t
        squirrels_dict = tuple()
        for index, lister in self.squirrels_list.items():
            squirrels_dict = squirrels_dict + ((index, tuple(lister)),)

        return Squirrels(variant_id=self.variant_id, pos=tuple(new_pos), squirrels_list=tuple(squirrels_dict), nuts_list=tuple(self.nuts_list.items()), nuts_left=tuple(new_nuts_left), hole_list=tuple(self.hole_list.items()), actual_hole_list=tuple(new_actual_hole_list.items()), hole_matching=tuple(self.hole_matching.items()))
        
        #return move
    
    @classmethod
    def isLegalPosition(cls, positionid):
        """Checks if the Puzzle is valid given the rules.
        For example, Hanoi cannot have a larger ring on top of a smaller one.
        Outputs:
            - True if Puzzle is valid, else False
        """
        return True
    

puzzle = Squirrels("starter")
#TUI(puzzle).play()
TUI(puzzle, solver=NoUndoSolver(puzzle), info=True).play()