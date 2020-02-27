# These are general functions that you might want to implement if you are to use the 
# PuzzlePlayer and the GeneralSolver

class Puzzle:
    
    # Intializer
    def __init__(self, variant_id=None, position_id=None):
        """
        Inputs:
            str: variant_id
            str: position_id
        """

    # Gameplay methods
    def __str__(self):
        """Returns the string representation of the puzzle.
        
        Outputs:
        String representation -- String
        """
        return "No String representation available"

    def primitive(self):
        """If the Puzzle is at an endstate, return GameValue.WIN or GameValue.LOSS
        else return GameValue.UNDECIDED

        GameValue located in the util class. If you're in the puzzles or solvers directory
        you can write from ..util import * 

        Outputs:
        Primitive of Puzzle type GameValue
        """
        raise NotImplementedError

    def doMove(self, move):
        """Given a valid move, returns a new Puzzle object with that move executed

        Inputs:
            move -- type defined by generateMoves

        Outputs:
            Puzzle with move executed
        """
        raise NotImplementedError

    def generateMoves(self):
        """Generate moves from self (including undos)

        Outputs:
        List of moves, move must be hashable
        """
        raise NotImplementedError

    def generateLegalMoves(self):
        """Generate only legal moves from self

        Outputs:
        List of moves, move must be hashable
        """
        return self.generateMoves()
    
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
    
    def generateSolutions(self):
        """Returns a list of Puzzle objects that are solved states

        Outputs:
        List of Puzzles
        """
        raise NotImplementedError

    # Server methods
    def encode(self):
        """Returns an id that can be decoded to create another Puzzle. Similar to a hash as
        that each encoding must be unique to each Puzzle state

        Outputs:
        Decodable id
        """
        raise NotImplementedError

    def getName(self):
        """Returns the name of the Puzzle.

        Outputs:
            String name
        """
        return self.__class__.__name__

    @staticmethod
    def checkValidVariant(position_id, variant_id):
        """Checks if the position is a possible position of variant given the 
        variant_id

        Inputs:
            position_id -- str
            variant_id -- str

        Outputs:
            True if possible else False
        """
        raise NotImplementedError