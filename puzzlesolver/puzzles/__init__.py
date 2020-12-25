from ._models import *

# Put your dependencies here
from .hanoi import Hanoi
from .lightsout import LightsOut
from .pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle
from .npuzzle import Npuzzle
from .chairs import Chairs
from .bishop import Bishop
from .topspin import TopSpin

# Add your puzzle in the puzzleList
puzzleList = {
    Npuzzle.puzzleid: Npuzzle,
    Hanoi.puzzleid: Hanoi,
    LightsOut.puzzleid: LightsOut,
    Peg.puzzleid: Peg,
    Chairs.puzzleid: Chairs,
    Bishop.puzzleid: Bishop,
    TopSpin.puzzleid: TopSpin,
}

class PuzzleManagerClass:
    """Controls what type of solver is applicable for a Puzzle and its variant"""

    def __init__(self, puzzleList):
        self.puzzleList = puzzleList

    def getPuzzleIds(self):
        """Returns a list of all the Puzzle ids"""
        return self.puzzleList.keys()

    def getPuzzleClasses(self):
        """Returns a list of all the Puzzle classes"""
        return self.puzzleList.values()

    def hasPuzzleId(self, puzzleid):
        """Checks if the puzzleid is located within the puzzleList"""
        return puzzleid in self.puzzleList
    
    def getPuzzleClass(self, puzzleid):
        """Basic getter method to "get" a Puzzle class"""
        return self.puzzleList[puzzleid]
    
    def getSolverClass(self, puzzleid, variant=None, test=False):
        # Check if variants or not
        puzzlecls = self.getPuzzleClass(puzzleid)
        if test and hasattr(puzzlecls, 'test_variants'):
            return puzzlecls.getSolverClass(variant=variant, test=False)
        if hasattr(puzzlecls, 'variants'):
            return puzzlecls.variants[variant]
        else:
            # TODO: Specific exception type
            raise Exception("Recommended solvers are not defined for the requested Puzzle")

PuzzleManager = PuzzleManagerClass(puzzleList)

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
