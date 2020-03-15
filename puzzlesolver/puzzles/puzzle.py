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
        """Given a valid move, returns a new Puzzle object with that move executed.
        Does nothing to the original Puzzle object
        
        NOTE: Must be able to take any move, including `undo` moves

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

    # Methods and attributes for Server
    """A dictionary with the following
    - variantId as the string key
    - A Solver class object as the value

    This dictionary is meant to store Solvers for the web server to interact with.
    See Hanoi for a dict comprehension example
    """
    variants = {}        

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, puzzleid, variantid, **kwargs):
        """Returns a Puzzle object based on puzzleid and
        variantid

        Example: puzzleid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        raise NotImplementedError

    def serialize(self, **kwargs):
        """Returns a serialized based on self

        Outputs:
            String Puzzle
        """
        raise NotImplementedError

    @classmethod
    def validate(cls, puzzleid, variantid, **kwargs):
        """Checks if the puzzleid fits the rules set for the puzzle, as
        well as fits the variantid as well
        
        Inputs:
            - puzzleid: 
            - variantid: 
        """
        raise NotImplementedError

    def generateMovePositions(self, movetype="legal", **kwargs):
        """Generate an iterable of puzzles with all moves fitting movetype
        executed.

        Inputs:
            -- movetype: The type of move to generate the puzzles
        
        Outputs:
            -- Iterable of puzzles 
        """
        puzzles = []
        for move in self.generateMoves(movetype=movetype, **kwargs):
            puzzles.append((move, self.doMove(move)))
        return puzzles