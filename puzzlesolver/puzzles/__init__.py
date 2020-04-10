from ._models import *

from .hanoi import Hanoi
from .graphpuzzle import GraphPuzzle

puzzleList = {
    Hanoi.puzzleid: Hanoi
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
