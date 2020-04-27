from ._models import *

from .hanoi import Hanoi
from .pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle
from .lightsout import LightsOut

puzzleList = {
    Peg.puzzleid: Peg,
    Hanoi.puzzleid: Hanoi,
    LightsOut.puzzleid: LightsOut
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
