# These are general functions that you might want to implement if you are to use the 
# PuzzlePlayer and the GeneralSolver

class Puzzle:
    
    # Intializer
    def __init__(self, **kwargs):
        pass

    # Gameplay methods
    def __str__(self):
        """Returns the string representation of the puzzle.
        
        Outputs:
        String representation -- String
        """
        return "No String representation available"

    def primitive(self, **kwargs):
        """If the Puzzle is at an endstate, return GameValue.WIN or GameValue.LOSS
        else return GameValue.UNDECIDED

        GameValue located in the util class. If you're in the puzzles or solvers directory
        you can write from ..util import * 

        Outputs:
        Primitive of Puzzle type GameValue
        """
        raise NotImplementedError

    def doMove(self, move, **kwargs):
        """Given a valid move, returns a new Puzzle object with that move executed

        Inputs:
            move -- type defined by generateMoves

        Outputs:
            Puzzle with move executed
        """
        raise NotImplementedError

    def generateMoves(self, movetype="all", **kwargs):
        """Generate moves from self (including undos)

        Inputs
        movetype -- str, can be the following
        - 'undo': undo moves
        - 'for': forward moves
        - 'bi': bidirectional moves
        - 'legal': legal moves (for + bi)
        - 'back': back moves (undo + bi)
        - 'all': all the moves listed above

        Outputs:
        Iterable of moves, move must be hashable
        """
        raise NotImplementedError

    # Solver methods
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
    
    def generateSolutions(self, **kwargs):
        """Returns a Iterable of Puzzle objects that are solved states

        Outputs:
        Iterable of Puzzles
        """
        raise NotImplementedError

    # Method for PickleSolverWrapper
    def getName(self, **kwargs):
        """Returns the name of the Puzzle.

        Outputs:
            String name
        """
        return self.__class__.__name__