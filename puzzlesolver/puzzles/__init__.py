from ._models import *

from .hanoi import Hanoi
from .lightsout import LightsOut
from .pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle
from .chairs import Chairs

puzzleList = {
    Hanoi.puzzleid: Hanoi,
    LightsOut.puzzleid: LightsOut,
    Peg.puzzleid: Peg,
    Chairs.puzzleid: Chairs
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
