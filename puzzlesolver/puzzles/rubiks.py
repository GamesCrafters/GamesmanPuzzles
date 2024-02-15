"""
File: rubiks.py
Puzzle: Rubik's Cube
Author: Mark Presten (Backend), Cameron Cheung (Backend, AutoGUI)
Date: September 14th, 2020
"""

import random
from . import ServerPuzzle
from ..util import *
import math

"""
    IMPLEMENTATION OF A 2x2x2 RUBIKS CUBE

          04 05                    1
          06 07                  0 2 4 5
    00 01 08 09 16 17 20 21        3
    02 03 10 11 18 19 22 23          L           B
          12 13                    F U B D     W R Y O
          14 15                      R           G

    F = front clockwise, F' = front counterclockwise
    B = back clockwise, B' = back counterclockwise,
    U = up, D = down, L = left, R = right

    MOVE ENCODING: 0=F,1=L,2=U,3=R,4=B,5=D, 6=F',7=L',8=U',9=R',10=B',11=D'
"""

# Rotations Matrix Example: 
# - On an F rotation,
#     1) 0 goes to 1 which goes to 3 which goes to 2 which goes to 0
#     2) 4 goes to 8 which goes to 12 wihch goes to 23 which goes to 4
#     3) 6 goes to 10 which goes to 14 which goes to 21 which goes to 0
# - On an F' rotation, 2 goes to 3 goes to 1 goes to 0 goes to 2, and so on...
# The rotations matrix is used for doMove()
rotations = [
    [0,1,3,2, 4,8,12,23, 6,10,14,21], # F
    [4,5,7,6, 0,20,16,8, 1,21,17,9], # L
    [8,9,11,10, 1,7,18,12, 3,6,16,13], # U
    [12,13,15,14, 2,10,18,22, 3,11,19,23], # R
    [16,17,19,18, 7,20,15,11, 5,22,13,9], # B
    [20,21,23,22, 0,14,19,5, 2,15,17,4], # D
]

move_names = ["F", "L", "U", "R", "B", "D", "F'", "L'", "U'", "R'", "B'", "D'"]

# There are 24 rotational symmetries of the rubiks cube. 
# For each of the 6 faces, you can move it to face downward, then rotate 4 times.
face_syms = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    [8, 9, 10, 11, 6, 4, 7, 5, 16, 17, 18, 19, 13, 15, 12, 14, 20, 21, 22, 23, 0, 1, 2, 3],
    [16, 17, 18, 19, 7, 6, 5, 4, 20, 21, 22, 23, 15, 14, 13, 12, 0, 1, 2, 3, 8, 9, 10, 11],
    [20, 21, 22, 23, 5, 7, 4, 6, 0, 1, 2, 3, 14, 12, 15, 13, 8, 9, 10, 11, 16, 17, 18, 19],
    [4, 5, 6, 7, 21, 23, 20, 22, 17, 19, 16, 18, 9, 11, 8, 10, 15, 14, 13, 12, 2, 0, 3, 1],
    [12, 13, 14, 15, 10, 8, 11, 9, 18, 16, 19, 17, 22, 20, 23, 21, 7, 6, 5, 4, 1, 3, 0, 2]
]

rot_syms = [2, 0, 3, 1, 23, 22, 21, 20, 4, 5, 6, 7, 8, 9, 10, 11, 17, 19, 16, 18, 15, 14, 13, 12]

syms = []
for face in face_syms:
    syms.append(face)
    for i in range(3):
        syms.append([syms[-1][rot_syms[i]] for i in range(24)])

corner_indices_arr = [[0,4,21], [1,6,8], [2,14,23], [3,10,12], [7,9,16], [5,17,20], [11,13,18], [15,19,22]]
corner_colors_arr = [[0,1,5], [0,1,2], [0,3,5], [0,2,3], [1,2,4], [1,4,5], [2,3,4], [3,4,5]]

starts = [ord(c) for c in 'agm']
start_idxs = [(0, 16), (4, 12), (8, 20)]

class Rubiks(ServerPuzzle):

    id = 'rubikscube'
    variants = ["2x2x2"]
    startRandomized = True

    def __init__(self, cube=None, **kwargs):
        if cube:
            self.cube = cube
        else:
            self.cube = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5]
            for _ in range(random.randint(15, 25)):
                self.cube = self.doMove(random.randint(0, 11)).cube

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself."""
        return "2x2x2"

    def primitive(self, **kwargs):
        return PuzzleValue.SOLVABLE if self.cube in [solution.cube for solution in self.generateSolutions()] else PuzzleValue.UNDECIDED

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype, **kwargs):
        if movetype in ('all', 'bi', 'legal', 'undo'):
            return list(range(12))
        else:
            return []

    def doMove(self, move, **kwargs):
        side = rotations[move % 6]
        cube = self.cube[:]
        direction = 1 if move < 6 else -1 # CW if move < 6 else CCW
        for i in range(3):
            for j in range(4):
                k1 = (i << 2) | j
                k2 = (i << 2) | ((j + direction) & 0b11)
                cube[side[k2]] = self.cube[side[k1]]
        return Rubiks(cube=cube)
    
    def h(cube):
        corner_ids, orientations = [], []
        for corner_indices in corner_indices_arr:
            corner_colors = sorted([cube[index] for index in corner_indices])
            corner_ids.append(corner_colors_arr.index(corner_colors))
            orientations.append(corner_colors.index(cube[corner_indices[0]]))
        h = 0
        corners = list(range(8))
        for i in range(8):
            h += corners.index(corner_ids[i]) * math.factorial(7 - i)
            corners.remove(corner_ids[i])
        return h * 2187 + sum([orientations[i]* 3**i for i in range(7)])

    def __hash__(self): # Return hash of the member that has the minimum hash within the cube's orbit
        min_hash = Rubiks.h(self.cube)
        for symmetry_id in range(1, 24):
            min_hash = min(min_hash, Rubiks.h([self.cube[i] for i in syms[symmetry_id]]))            
        return min_hash
        
    def generateSolutions(self, **kwargs):
        solved_cubes = [
            [0,1,2,3,4,5], [0,2,3,5,4,1], [0,3,5,1,4,2], [0,5,1,2,4,3],
            [1,4,2,0,3,5], [1,2,0,5,3,4], [1,0,5,4,3,2], [1,5,4,2,3,0],
            [2,4,3,0,5,1], [2,3,0,1,5,4], [2,0,1,4,5,3], [2,1,4,3,5,0],
            [3,4,5,0,1,2], [3,5,0,2,1,4], [3,0,2,4,1,5], [3,2,4,5,1,0],
            [4,5,3,2,0,1], [4,3,2,1,0,5], [4,2,1,5,0,3], [4,1,5,3,0,2],
            [5,1,0,3,2,4], [5,0,3,4,2,1], [5,3,4,1,2,0], [5,4,1,0,2,3]
        ]
        return [Rubiks(cube=sum([[c] * 4 for c in sc], [])) for sc in solved_cubes]

    ### ________ Server _________
    @classmethod
    def fromHash(cls, variantid, hash_val):
        """ 
        Note that this function does not actually unhash the given hash value
        because the hash method we used here is irreversible. Since this
        method is only used to generate random positions of a puzzle, we
        instead return a position that is already randomized by the constructor
        of a Rubiks instance.
        """
        return cls()

    @classmethod
    def fromString(cls, variant_id, position_str):
        """Returns a Puzzle object based on positionid
        Inputs:
            positionid - String id from puzzle
        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        return Rubiks([int(k) for k in position_str])

    def toString(self, mode):
        """Returns a position string
        Outputs:
            String Puzzle
        """
        prefix = ''
        if mode == StringMode.AUTOGUI:
            entity_string = self.cube[:]
            prefix = '1_'
            for i in range(3):
                for k in range(start_idxs[i][0], start_idxs[i][0] + 4):
                    entity_string[k] = chr(self.cube[k] + starts[i])
                for k in range(start_idxs[i][1], start_idxs[i][1] + 4):
                    entity_string[k] = chr(self.cube[k] + starts[i])
        else:
            entity_string = [str(k) for k in self.cube]
        return prefix + ''.join(entity_string)
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            i = 24 + (move << 1)
            return f'M_{i}_{i + 1}_x'
        else:
            return move_names[move]

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
        
        Will return a random Rubiks instance.
        """
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Rubiks.variants: raise IndexError("Out of bounds variantid")
        return Rubiks(cube=None) # return random cube