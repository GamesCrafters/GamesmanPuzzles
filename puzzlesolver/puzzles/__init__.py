from ._models import *

from .hanoi import Hanoi
from .pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle

puzzleList = {
    Peg.puzzleid: Peg,
    Hanoi.puzzleid: Hanoi
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
