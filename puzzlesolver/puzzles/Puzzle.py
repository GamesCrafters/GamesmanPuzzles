# These are general functions that you might want to implement if you are to use the PuzzlePlayer
# and the GeneralSolver

class Puzzle:

    def primitive(self):
        """If the Puzzle is at an endstate, return GameValue.WIN or GameValue.LOSS
        else return GameValue.UNDECIDED

        GameValue located in the util class. If you're in the puzzles directory
        you can write from ..util import * 

        Outputs:
        Primitive of Puzzle type GameValue
        """
        raise NotImplementedError

    def doMove(self, move):
        """Given a valid move, returns a new Puzzle object with that move executed

        Inputs
        move -- any type (defined by generateMoves)

        Outputs:
        Puzzle with move executed
        """
        raise NotImplementedError

    def generateMoves(self):
        """Generate possible moves from the self

        Outputs:
        List of moves
        """
        raise NotImplementedError

    def winStates(self):
        """Returns a list of Puzzle objects that are wins

        Outputs:
        List of Puzzles
        """
        raise NotImplementedError