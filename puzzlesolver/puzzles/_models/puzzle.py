# These are general functions that you might want to implement if you are to use the 
# PuzzlePlayer and the GeneralSolver
from ...util import classproperty, deprecated, StringMode
import progressbar
import warnings

class Puzzle:
    id = None
    startRandomized = False

    #################################################################
    # Initializer
    #################################################################

    def __init__(self):
        """Returns an instance of a Puzzle. Board state of the Puzzle
        should be a Puzzle returned from `generateStartPosition`
        """
        pass

    #################################################################
    # Variants
    #################################################################

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself.

        Example: '5x5', '3x4', 'reverse3x3'
        """
        return "NA"

    @classmethod
    def generateStartPosition(cls, variantid):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        raise NotImplementedError

    #################################################################
    # String representations
    #################################################################

    def toString(self, mode=StringMode.HUMAN_READABLE):
        """Returns the string representation of the Puzzle based on the type. 

        If mode is "minimal", 
        If mode is "complex",

        Inputs:
            mode -- "minimal", "complex"
        
        Outputs:
            String representation -- String"""
        
        return self.toString(mode)

    def __str__(self):
        """Returns the toString representation in "complex" mode

        Returns
        -------
        str
            self.toString(mode="complex")
        """
        return self.toString(mode="complex")
    
    def moveString(self, move, mode):
        """Returns the string representation of the move based on the type.

        If mode is "uwapi", return a UWAPI movestring.
        If mode is "humanreadable", return a human-readable movestring.

        Inputs:
            mode -- "uwapi", "humanreadable"
        Outputs:
            String representation of move -- String"""
        
        return str(move)

    #################################################################
    # Gameplay methods
    #################################################################

    def primitive(self):
        """If the Puzzle is at an endstate, return PuzzleValue.SOLVABLE or PuzzleValue.UNSOLVABLE
        else return PuzzleValue.UNDECIDED

        PuzzleValue located in the util class. If you're in the puzzles or solvers directory
        you can write from ..util import * 

        Outputs:
            Primitive of Puzzle type PuzzleValue
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def generateMoves(self, movetype="legal"):
        """Generate moves from self (including undos)

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
        raise NotImplementedError

    #################################################################
    # Solver methods
    #################################################################

    def __hash__(self):
        """Returns a hash of the puzzle.
        Requirements:
        - Each different puzzle must have a different hash
        - The same puzzle must have the same hash.
        
        Outputs:
            Hash of Puzzle -- Integer

        Note: How same and different are defined are dependent on how you implement it.
        For example, a common optimization technique for reducing the size of key-value
        pair storings are to make specific permutations of a board the same as they have
        the same position value (i.e. rotating or flipping a tic-tac-toe board). 
        In that case, the hash of all those specific permutations are the same.
        """
        raise NotImplementedError

    @property
    def numPositions(self):
        """Returns the max number of possible positions from the solution state.
        Main use is for the progressbar module. 
        Default is unknown length, can be overwritten
        """
        return None

    def generateSolutions(self):
        """Returns a Iterable of Puzzle objects that are solved states.
        Not required if noGenerateSolutions is true, and using a CSP-implemented solver.

        Outputs:
            Iterable of Puzzles
        """
        return []

    #################################################################
    # Player methods
    #################################################################

    def playPuzzle(self, moves):
        """Default playPuzzle method uses indices to chose which
        move to play."""

        print("Possible Moves:")
        for count, m in enumerate(moves):
            print(str(count) + " -> " + str(m))
        print("Enter Piece: ")
        index = int(input())
        if index == '':
            return "BEST"
        elif index >= len(moves):
            return "OOPS"
        else:
            return moves[index]

    #################################################################
    # Number representation
    #################################################################

    def __add__(self, other):
        """Equivalent to doMove, can only add moves together

        Parameters
        ----------
        other : "Move"
            Custom defined Puzzle move

        Returns
        -------
        Puzzle
            Puzzle instance with move executed
        """
        return self.doMove(other)

    def __radd__(self, other):
        """Reverse add (same as __add__)

        Parameters
        ----------
        other : "Move"
            Custom defined Puzzle move

        Returns
        -------
        Puzzle
            Puzzle instance with move exectuted        
        """
        return self.doMove(other)

    def __repr__(self):
        return "<{} object with {}>".format(self.__class__.__name__, self.toString(mode="minimal"))

    #################################################################
    # Deprecated methods
    #################################################################

    def printInfo(self):
        """Prints the string representation of the puzzle. 
        Can be custom defined"""
        
        return str(self)