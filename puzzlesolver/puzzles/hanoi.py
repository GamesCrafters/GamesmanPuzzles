"""Game for Tower of Hanoi
https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import IndexSolver

def ffs(num):
    """Helper function to return the index of the LSB. 
    For the 0 case, return `float('inf')`
    """
    output = (num & -num).bit_length() - 1
    output = output if output != -1 else float('inf')
    return output

class Hanoi(ServerPuzzle):

    id      = 'hanoi'
    auth    = "Anthony Ling"
    name    = "Towers of Hanoi"
    desc    = """Move smaller discs ontop of bigger discs. 
        Fill the rightmost stack."""
    date    = "April 2, 2020"

    variants =  ["2_1"]
    variants += ["3_1", "3_2", "3_3", "3_4", "3_5", "3_6", "3_7", "3_8"]
    variants += ["4_1", "4_2", "4_3", "4_4", "4_5", "4_6"]
    variants += ["5_1", "5_2", "5_3", "5_4"]

    test_variants = ["3_1", "3_2", "3_3"]

    def __init__(self,  variantid=None, variant=None):
        """Returns the starting position of Hanoi based on variant first, then 
        variantID. By default it follows "3_3"

        Inputs 
            - (Optional) variantid: string
            - (Optional) variant: dict

        Outputs
            - A Puzzle of Hanoi
        """
        self.rod_variant = 3
        self.disk_variant = 3
        if variant:
            if not isinstance(variant, dict):
                raise TypeError("Variant keyword argument is not of type dict")
            if "rod_variant" not in variant:
                raise ValueError("Variant keyword argument does not contain rod_variant")
            if "disk_variant" not in variant:
                raise ValueError("Variant keyword argument does not contain disk_variant")
            self.rod_variant, self.disk_variant = variant["rod_variant"], variant["disk_variant"]
        elif variantid:
            if not isinstance(variantid, str):
                raise TypeError("VariantID is not of type str")
            strlist = variantid.split("_")
            if len(strlist) != 2:
                raise ValueError("Invalid variantID")
            self.rod_variant = int(strlist[0])
            self.disk_variant = int(strlist[1])

        self.rods = [2 ** self.disk_variant - 1] + [0] * (self.rod_variant - 1)
    
    @property
    def variant(self):
        """Returns the variant of the Puzzle
        
        Outputs:
        - Variant : str
        """
        return "{}_{}".format(self.rod_variant, self.disk_variant)

    @property
    def numPositions(self):
        """Returns the upperbound number of possible hashes

        Outputs:
        - numPositions : int
        """
        return self.rod_variant ** self.disk_variant

    def __hash__(self):
        """Returns the reduced hash of the Puzzle
        
        Outputs:
        - hash : int
        """

        # Except for the last rod, sort all the rods in descending order by size
        rodscopy = self.rods[:-1]
        rodscopy.sort(reverse=True)

        # Hash calculation is the sum of the:
        #   rod index of a disk * rod_variant ** disk size
        # over all disks  
        output = 0
        for i in range(len(rodscopy)):
            rod = rodscopy[i]
            j = 0
            while rod != 0:
                mod = rod % 2
                output += mod * (i + 1) * self.rod_variant ** j
                j += 1
                rod = rod >> 1
        return output

    def toString(self, mode="minimal"):
        """Returns the string representation of the Puzzle based on the type. 

        If mode is "minimal", return the serialize() version
        If mode is "complex", return the printInfo() version

        Inputs:
            mode -- "minimal", "complex"
        
        Outputs:
            String representation -- String"""
        
        if mode == "minimal":
            return "-".join([str(rod) for rod in self.rods])
        elif mode == "complex":
            # Easier to convert to a list of lists and use
            # [6, 1, 0] -> [["C", "B"], ["A"], []]
            letters = []
            for rod in self.rods:
                stack = []
                for j in range(self.disk_variant):
                    if (rod >> j) % 2 == 1:
                        stack = [chr(j + 65)] + stack
                letters.append(stack)

            # Convert the list of lists into string representation
            output = ""
            for j in range(self.disk_variant): 
                row = ""
                for stack in letters:
                    row += " " * 3
                    if len(stack) > j: row += stack[j]
                    else: row += "|"
                output = row + "\n" + output
            output += "----" * (self.rod_variant) + "---\n"
            output += "   " + "   ".join(str(i) for i in range(0, self.rod_variant))
            return output
        else:
            raise ValueError("Invalid keyword argument 'mode'")
    
    @classmethod
    def fromString(cls, positionid : str):
        """Returns a Puzzle object based on "minimal"
        String representation of the Puzzle (i.e. `toString(mode="minimal")`)

        Example: positionid="6-1-0" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Must raise a TypeError if the positionid is not a String
        Must raise a ValueError if the String cannot be translated into a Puzzle
        
        NOTE: A String cannot be translated into a Puzzle if it leads to an illegal
        position based on the rules of the Puzzle

        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        if not isinstance(positionid, str):
            raise TypeError("PositionID is not type str")
        
        rod_strings = positionid.split("-")
        if not rod_strings:
            raise ValueError("PositionID cannot be translated into Puzzle")
        
        try:
            rods = [int(rod) for rod in rod_strings]
        except ValueError:
            raise ValueError("PositionID cannot be translated into Puzzle")

        sum_rods = sum(rods) + 1
        if sum_rods & -sum_rods != sum_rods:
            raise ValueError("PositionID cannot be translated into Puzzle")

        newPuzzle = Hanoi(variant={
            "rod_variant" : len(rods), 
            "disk_variant" : sum_rods.bit_length() - 1})
        newPuzzle.rods = rods
        return newPuzzle

    def __repr__(self):
        """Returns the string representation of the Puzzle as a 
        Python object
        """
        return "Hanoi(board={})".format(self.toString())

    def primitive(self):
        """If the Puzzle is at an endstate, return PuzzleValue.SOLVABLE or PuzzleValue.UNSOLVABLE
        else return PuzzleValue.UNDECIDED

        PuzzleValue located in the util class. If you're in the puzzles or solvers directory
        you can write from ..util import * 

        Outputs:
            Primitive of Puzzle type PuzzleValue
        """
        if self.rods[-1] != 2 ** self.disk_variant - 1:
            return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE

    def doMove(self, move):
        """Given a valid move, returns a new Puzzle object with that move executed.
        Does nothing to the original Puzzle object
        
        NOTE: Must be able to take any move, including `undo` moves

        Raises a TypeError if move is not of the right type
        Raises a ValueError if the move is not in generateMoves

        Inputs
            move -- type defined by generateMoves

        Outputs:
            Puzzle with move executed
        """

        if not isinstance(move, tuple) and \
            len(move) != 2 and \
            isinstance(move[0], int) and \
            isinstance(move[1], int):
            raise TypeError("Invalid type for move")

        if move not in self.generateMoves(): 
            raise ValueError("Move not possible")

        newPuzzle = Hanoi(variantid=self.variant)
        rods = self.rods.copy()

        lsb_index = ffs(rods[move[0]])
        assert lsb_index != float('inf')
        rods[move[0]] = rods[move[0]] - (1 << lsb_index)
        rods[move[1]] = rods[move[1]] + (1 << lsb_index)
        assert sum(rods) == 2 ** self.disk_variant - 1
        newPuzzle.rods = rods
        return newPuzzle        

    def generateMoves(self, movetype="all"):
        """Generate moves from self (including undos). 
        NOTE: For Hanoi, all moves are bidirectional, so movetype doens't matter

        Inputs
            movetype -- str, can be the following
            - 'for': forward moves
            - 'bi': bidirectional moves
            - 'back': back moves
            - 'legal': legal moves (for + bi)
            - 'undo': undo moves (back + bi)
            - 'all': any defined move (for + bi + back)

        Outputs:
            Iterable of moves, move must be hashable
        """
        moves = set()
        rods = list(map(ffs, self.rods))
        for i in range(len(rods)):
            for j in range(len(rods)):
                if rods[i] < rods[j]:
                    moves.add((i, j))
        return moves

    def generateSolutions(self):
        """Returns a Iterable of Puzzle objects that are solved states.
        Not required if noGenerateSolutions is true, and using a CSP-implemented solver.

        Outputs:
            Iterable of Puzzles
        """
        puzzle_string = "0-" * (self.rod_variant - 1)
        puzzle_string += str(2 ** self.disk_variant - 1)

        return [self.fromString(puzzle_string)]

    @classmethod
    def generateStartPosition(cls, variantid, variant=None):
        """Returns the starting position of Hanoi based on variant first, then 
        variantID. Follows the same functionality as __init__

        Inputs 
            - (Optional) variantid: string
            - (Optional) variant: dict

        Outputs
            - A Puzzle of Hanoi
        """
        return Hanoi(variantid, variant)
