from ._models import *

from .hanoi import Hanoi
from .graphpuzzle import GraphPuzzle
from .npuzzle import Npuzzle

puzzleList = {
    Hanoi.puzzleid: Hanoi,
    Npuzzle.puzzleid: Npuzzle
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
