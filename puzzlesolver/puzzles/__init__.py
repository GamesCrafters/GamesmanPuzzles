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

class PuzzleManager:
    """Controls what type of solver is applicable for a Puzzle and its variant"""

    @staticmethod
    def getPuzzleClass(puzzleid):
        """Basic getter method to "get" a Puzzle class"""
        return puzzleList[puzzleid]
    
    @staticmethod
    def getSolverClass(puzzleid, variant, test=False):
        # Check if variants or not
        puzzlecls = PuzzleManager.getPuzzleClass(puzzleid)
        if test and hasattr(puzzlecls, 'test_variants'):
            return puzzlecls.test_variants[variant]
        if hasattr(puzzlecls, 'variants'):
            return puzzlecls.variants[variant]
        else:
            # TODO: Specific exception type
            raise Exception("Recommended solvers are not defined for the requested Puzzle")
        
for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
