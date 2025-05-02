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

#from ..util import *
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
    variants = ['starter', 'junior', 'expert', 'master', 'wizard']
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
            for i, piece in enumerate(self.pos):
                if " " in piece:
                    nut_part = piece.split(" ")[0]
                    hole_part = piece.split(" ")[1]

                    # for hole
                    hole_type, hole_type_index, hole_relation = hole_part.split("_")
                    self.hole_list[hole_type_index] = hole_relation
                    self.hole_matching[i] = hole_part

                    # for nut
                    type, type_index, relation, orientation = nut_part.split("_")
                    if relation == "O":
                        self.nuts_left.append(nut_part)
                        self.nuts_list[type_index] = nut_part
                    if type_index not in self.squirrels_list:
                        self.squirrels_list[type_index] = []
                    self.squirrels_list[type_index].append(nut_part)
                elif "H" in piece: # means we have a hole
                    type, type_index, relation = piece.split("_")
                    self.hole_list[type_index] = relation
                    self.hole_matching[i] = piece
                elif "N" in piece: # means this is a nut piece
                    type, type_index, relation, orientation = piece.split("_")
                    if relation == "O":
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
        stringpos = self.toString(StringMode.AUTOGUI)
        stringpos = stringpos[2:]
        hash = 0
        charmap = {
            'T': 0,
            't': 1,
            '1': 2,
            'R': 3,
            'r': 4,
            '2': 5,
            'B': 6,
            'b': 7,
            '3': 8,
            'L': 9,
            'l': 10,
            '4': 11,
            'A': 12,
            '5': 12,
            '6': 12,
            '7': 12,
            '8': 12,
            '9': 12,
            'H': 13,
            'X': 14,
            '-': 15
        }
        for char in stringpos:
            hash <<= 4
            hash += charmap[char]
        return hash

    @classmethod
    def fromString(cls, variant_id, board_string):
        # Checking if the positionid is a str
        if not board_string or not isinstance(board_string, str):
            raise TypeError("PositionID is not type str")
        # Checking if this is a valid string (extract the board and difficulty first)
        new_board_string = board_string.split('|')
        new_pos = []
        for i, word in enumerate(new_board_string):
            if "D" in word:
                indexer = word.index("D")
                new_word = word[:indexer - 1]
                new_pos.append(new_word)
            else:
                new_pos.append(word)
        # Check that this will decode into a valid board
        new_squirrels_list = {}
        new_nuts_list = {}
        new_nuts_left = []
        new_hole_list = {}
        new_hole_matching = {}
        new_actual_hole_list = {}
        dropped_nut = None
        for i, piece in enumerate(new_board_string):
            if " " in piece:
                nut_part = piece.split(" ")[0]
                hole_part = piece.split(" ")[1]
                # for hole
                if "D" in piece:
                    hole_type, hole_type_index, hole_relation, dropped_nut = hole_part.split("_")
                else:
                    hole_type, hole_type_index, hole_relation = hole_part.split("_")
                new_hole_list[hole_type_index] = hole_relation
                new_hole_matching[i] = hole_part
                if dropped_nut is not None:
                    dropped_nut_str = "N_" + dropped_nut[1]
                    if dropped_nut_str not in new_actual_hole_list.values():
                        new_actual_hole_list[i] = dropped_nut_str
                # for nut
                type, type_index, relation, orientation = nut_part.split("_")
                if relation == "O":
                    new_nuts_list[type_index] = nut_part
                if type_index not in new_squirrels_list:
                    new_squirrels_list[type_index] = []
                new_squirrels_list[type_index].append(nut_part)
            elif "H" in piece: # means we have a hole
                dropped_nut = None
                if "D" in piece:
                    hole_type, hole_type_index, hole_relation, dropped_nut = piece.split("_")
                else:
                    hole_type, hole_type_index, hole_relation = piece.split("_")
                #type, type_index, relation = piece.split("_")
                new_hole_list[hole_type_index] = hole_relation
                new_hole_matching[i] = piece
                if dropped_nut is not None:
                    dropped_nut_str = "N_" + dropped_nut[1]
                    if dropped_nut_str not in new_actual_hole_list.values():
                        new_actual_hole_list[i] = dropped_nut_str
            elif "N" in piece: # means this is a nut piece
                type, type_index, relation, orientation = piece.split("_")
                if relation == "O":
                    new_nuts_list[type_index] = piece
                if type_index not in new_squirrels_list:
                    new_squirrels_list[type_index] = []
                new_squirrels_list[type_index].append(piece)
        for squirrel_nut in new_nuts_list.values():
            type, type_index, relation, orientation = squirrel_nut.split("_")
            if (type + "_" + type_index) not in new_actual_hole_list.values():
                new_nuts_left.append(squirrel_nut)
        # If no error, we can return a board with the given puzzle.
        squirrels_dict = tuple()
        for index, lister in new_squirrels_list.items():
            squirrels_dict = squirrels_dict + ((index, tuple(lister)),)
        return Squirrels(variant_id=variant_id, pos=tuple(new_pos), squirrels_list=tuple(squirrels_dict), nuts_list=tuple(new_nuts_list.items()), nuts_left=tuple(new_nuts_left), hole_list=tuple(new_hole_list.items()), actual_hole_list=tuple(new_actual_hole_list.items()), hole_matching=tuple(new_hole_matching.items()))
    
    def toString(self, mode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle position -- String
        """
        display = ""
        #temp = []
        #for i in range(16):
        """
        for i in range(4):
            display += str(self.pos[4 * i:4 * (i + 1)]) + "\n"
        return display
        """
        '''
        6,7,8,9 = acorn in hole on board
        H = hole
        l = left empty squirrel piece
        L = left squirrel piece
        r = right empty squirrel piece
        R = right squirrel piece
        t = top empty squirrel piece
        T = top squirrel piece
        b = bottom empty squirrel piece
        B = bottom squirrel piece
        1 = top squirrel piece with nut
        2 = right squirrel piece with nut
        3 = bottom squirrel piece with nut
        4 = left squirrel piece with nut
        X = block
        - = empty
        '''
        if mode == StringMode.AUTOGUI:
            outlist = ['-'] * 16
            for i, piece in enumerate(self.pos):
                if piece[0] == '-':
                    continue
                if piece[0] == 'H':
                    outlist[i] = 'H'
                    if i in self.actual_hole_list.keys():
                        acorn_num = int(self.actual_hole_list[i][2])
                        acorn_num += 5
                        outlist[i] = str(acorn_num)
                if piece[0] == 'N':
                    if " " in piece:
                            piece = piece.split(" ")[0]
                    if i - 1 >= (i // 4) * 4 and self.pos[i - 1][0] == 'N' and piece[:3] == self.pos[i - 1][:3]:
                        if piece[4] == 'O':
                            if piece in self.nuts_left:
                                outlist[i] = '2'
                            else:
                                outlist[i] = 'r'
                        else:
                            outlist[i] = 'R'
                    elif i - 4 >= 0 and self.pos[i - 4][0] == 'N' and piece[:3] == self.pos[i - 4][:3]:
                        if piece[4] == 'O':
                            if piece in self.nuts_left:
                                outlist[i] = '3'
                            else:
                                outlist[i] = 'b'
                        else:
                            outlist[i] = 'B'
                    elif i + 1 < ((i // 4 + 1) * 4) and self.pos[i + 1][0] == 'N' and piece[:3] == self.pos[i + 1][:3]:
                        if piece[4] == 'O':
                            if piece in self.nuts_left:
                                outlist[i] = '4'
                            else:
                                outlist[i] = 'l'
                        else:
                            outlist[i] = 'L'
                    elif i + 4 < 16 and self.pos[i + 4][0] == 'N' and piece[:3] == self.pos[i + 4][:3]:
                        if piece[4] == 'O':
                            if piece in self.nuts_left:
                                outlist[i] = '1'
                            else:
                                outlist[i] = 't'
                        else:
                            outlist[i] = 'T'
                if piece[0] == 'B':
                    outlist[i] = 'X'
            return '1_' + ''.join(outlist)
        else:
            line = []
            for i, piece in enumerate(self.pos):
                if " " in piece:
                    nut_part = piece.split(" ")[0]
                    hole_part = piece.split(" ")[1]
                    if i in self.actual_hole_list.keys() and "D" not in piece:
                        _, nut_dropped = self.actual_hole_list[i].split("_")
                        hole_part = hole_part + "_D" + nut_dropped
                    # for hole
                    # for nut
                    line.append(nut_part + " " + hole_part)
                elif "H" in piece:
                    type, type_index, relation = piece.split("_")
                    if i in self.actual_hole_list.keys() and "D" not in piece:
                        _, nut_dropped = self.actual_hole_list[i].split("_")
                        new_piece = piece + "_D" + nut_dropped
                        line.append(new_piece)
                    else:
                        line.append(piece)
                else:
                    line.append(piece)
            return '|'.join(line)




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
            if " " in piece:
                piece = piece.split(" ")[0]
            if piece in self.nuts_list.values(): # checks if its a squirrel + nut -> can enumerate from there with squirrel index
                type, type_index, relation, orientation = piece.split("_")
                if type_index not in checked_squirrel:
                    num_blocks = len(self.squirrels_list[type_index])
                    # will need to check if the move is also a hole -> can move into holes as well as a move
                    # checks if leftward move possible
                    count = []
                    for squirrel_block in self.squirrels_list[type_index]:
                        Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                        Sorientation = int(Sorientation)
                        if (i + Sorientation) % 4 > 0:
                            left_block = self.pos[i + Sorientation - 1]
                            # if hole or empty or part of this squirrel, we can move
                            if len(left_block) == 5 or left_block == '-' or (Stype + "_" + Stype_index) in left_block: 
                                count.append(f"M_{i + Sorientation}_{i + Sorientation - 1}_{squirrel_block}") # Move, curr, next, nut index
                            
                    if len(count) == num_blocks: # if all blocks can move for the squirrel
                        moves.append(count)
                       
                    # checks if rightward move possible
                    count = []
                    for squirrel_block in self.squirrels_list[type_index]:
                        Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                        Sorientation = int(Sorientation)
                        if (i + Sorientation) % 4 < 3:
                            right_block = self.pos[i + 1 + Sorientation]
                            if len(right_block) == 5 or right_block == "-" or (Stype + "_" + Stype_index) in right_block:
                                count.append(f"M_{i + Sorientation}_{i + 1 + Sorientation}_{squirrel_block}") # CHECK HERE COULD BE SUS
                    if len(count) == num_blocks:
                        moves.append(count)
                        
                    
                    count = []
                    for squirrel_block in self.squirrels_list[type_index]:
                    # Check for upward moves
                        Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                        Sorientation = int(Sorientation)
                        if (i+Sorientation) - 4 >= 0:
                            up_block = self.pos[(i + Sorientation) - 4]
                            if len(up_block) == 5  or up_block == "-" or (Stype + "_" + Stype_index) in up_block:
                                count.append(f"M_{i + Sorientation}_{(i + Sorientation) - 4}_{squirrel_block}")
                    if len(count) == num_blocks:
                        moves.append(count)   
                       
                       
                    count = []
                    for squirrel_block in self.squirrels_list[type_index]:
                    # Check for downward moves
                        Stype, Stype_index, Srelation, Sorientation = squirrel_block.split("_")
                        Sorientation = int(Sorientation)
                        if (i + Sorientation) + 4 < 16:
                            down_block = self.pos[(i + Sorientation) + 4]
                            if len(down_block) == 5 or down_block == "-" or (Stype + "_" + Stype_index) in down_block:
                                count.append(f"M_{i + Sorientation}_{(i + Sorientation) + 4}_{squirrel_block}")
                    if len(count) == num_blocks:
                        moves.append(count)
                        
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
            _, start, end, type, type_index, relation, orientation = piece.split("_")
            start = int(start)
            end = int(end)
            # Make sure to adjust when a nut is in a hole
            # First check the move's orientation to know which way to move
            # check if new piece has hole -> means it needs to be updated into the hole placements
            piece_string = type+"_"+type_index+"_"+relation+"_"+orientation
            new_pos[end] = piece_string
            if end in self.hole_coords:
                new_pos[end] = piece_string + " " + self.hole_matching[end] # MUST BE NUT + HOLE ALWAYS
                if self.nuts_list[type_index] in new_nuts_left and relation == "O" and end not in new_actual_hole_list: 
                # CHECK THIS UPDATE: now checks if hole and if still usable hole for nuts -> past code (self.pos[end] in self.hole_matching.values())
                # WAIT should check if the hole is already filled??
                    acorn_str = type + "_" + type_index
                    if acorn_str not in new_actual_hole_list.values():
                        new_actual_hole_list[end] = acorn_str # hole location : nut index
                        new_nuts_left.remove(self.nuts_list[type_index]) # takes the nuts on the board off -> no more nut to consider
            if start not in self.hole_coords and not (len(new_pos[start]) >= 7 and new_pos[start] != piece_string): # needs to check that it is not a nut
                new_pos[start] = "-"
            if start in self.hole_coords and self.pos[start] == new_pos[start]: # if there was a hole here
                if " " in new_pos[start]:
                    nut_part = new_pos[start].split(" ")[0]
                    hole_part = new_pos[start].split(" ")[1]
                    new_pos[start] = hole_part
                    new_pos[end] = nut_part
                else:
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

    def moveString(self, move, mode):
        # move is a collection of the moves from generation string in a single list
        # want to join move into a string
        # in each move, each piece needs to be converted into a single string split by | character
        # ('M_10_2_N_2_O_0', 'M_14_6_N_2_X_4') -> 'M_10_2_N_2_O_0|M_14_6_N_2_X_4'
        if mode == StringMode.HUMAN_READABLE:
            return '|'.join(move)
        else:
            movelist = move[0].split('_')
            guimove = 'M_' + str(movelist[1]) + '_' + str(movelist[2]) + '_x'
            return guimove
            

#puzzle = Squirrels("starter")
#TUI(puzzle).play()
#TUI(puzzle, solver=NoUndoSolver(puzzle), info=True).play()