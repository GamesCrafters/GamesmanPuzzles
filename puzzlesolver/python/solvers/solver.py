#These are general functions that you might want to implement if you are to use the PuzzlePlayer
from ..util import *

class Solver:

    def __init__(self, puzzle, **kwargs):
        """Creates a Solver object initialized with puzzle

        Inputs
        puzzle -- the puzzle to be solved on
        """
        raise NotImplementedError

    def solve(self, *args, **kwargs):
        """Solves the puzzle initialized in the init function
        """
        raise NotImplementedError
    
    def getRemoteness(self, puzzle, **kwargs):
        """Finds the remoteness of the puzzle

        Inputs:
        puzzle -- the puzzle in question

        Outputs:
        remoteness of puzzle
        """
        raise NotImplementedError

    # Built-in functions
    def getValue(self, puzzle, **kwargs):
        """Returns solved value of the puzzle

        Inputs
        puzzle -- the puzzle in question

        Outputs:
        value of puzzle
        """
        remoteness = self.getRemoteness(puzzle, **kwargs)
        if remoteness == PuzzleValue.UNSOLVABLE: return PuzzleValue.UNSOLVABLE
        return PuzzleValue.SOLVABLE