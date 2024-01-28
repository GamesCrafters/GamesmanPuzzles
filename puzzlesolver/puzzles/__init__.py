from ._models import *
from ..solvers import IndexSolver, PickleSolver, LightsOutClosedFormSolver
from ..util import PuzzleException

# Put your dependencies here
from .hanoi import Hanoi
from .lightsout import LightsOut
from .pegSolitaire import Peg
from .npuzzle import Npuzzle
from .toadsandfrogspuzzle import ToadsAndFrogsPuzzle
from .bishop import Bishop
from .topspin import TopSpin
from .hopNdrop import HopNDrop
from .rubiks import Rubiks
from .nqueens import NQueens
from .rushhour import RushHour
#from .examplepuzzle import ExamplePuzzle

# Add your puzzle in the puzzleList
puzzleList = {
    #ExamplePuzzle.id: ExamplePuzzle,
    Bishop.id:      Bishop,
    Hanoi.id:       Hanoi,
    HopNDrop.id:    HopNDrop,
    LightsOut.id:   LightsOut,
    Npuzzle.id:     Npuzzle,
    NQueens.id:     NQueens,
    Peg.id:         Peg,
    ToadsAndFrogsPuzzle.id:      ToadsAndFrogsPuzzle,
    TopSpin.id:     TopSpin,
    Rubiks.id:      Rubiks,
    RushHour.id:    RushHour
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
    
    def getSolverClass(self, puzzleid, variantid=None, test=False):
        """Get Solver Class given the puzzleid"""
        if puzzleid == RushHour.id or puzzleid == TopSpin.id:
            return PickleSolver
        if puzzleid == LightsOut.id:
            if variantid in LightsOut.closed_form_variants:
                return LightsOutClosedFormSolver
            return IndexSolver
        return IndexSolver
    
    def validate(self, puzzleid, variantid=None, positionid=None):
        """Checks if the positionid fits the rules set for the puzzle, as
        well as if it's supported by the app.
        
        Raises a PuzzleException for the following:
        - puzzleid is not implemented
        - variantid is not the proper Type
        - variantid is not part of the puzzle implementation
        - fromString doesn't raise a Exception

        Inputs:
            - puzzleid
            - positionid: 
            - variantid: 
        """
        if puzzleid not in puzzleList:
            raise PuzzleException("Invalid PuzzleID")

        puzzlecls = self.puzzleList[puzzleid]
        if variantid is not None:
            if not isinstance(variantid, str): 
                raise PuzzleException("Invalid VariantID")
            if variantid not in puzzlecls.variants:
                raise PuzzleException("Out of bounds VariantID")
        
        if positionid is not None:
            try:
                puzzle = puzzlecls.fromString(variantid, positionid)
            except (ValueError, TypeError):
                raise PuzzleException("Invalid PositionID")

            if variantid is not None and puzzle.variant != variantid:
                raise PuzzleException("VariantID doesn't match PuzzleID")

PuzzleManager = PuzzleManagerClass(puzzleList)

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
