from ._models import *

from .hanoi import Hanoi
from .lightsout import LightsOut
from .graphpuzzle import GraphPuzzle

puzzleList = {
    Hanoi.puzzleid: Hanoi,
    LightsOut.puzzleid: LightsOut
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
