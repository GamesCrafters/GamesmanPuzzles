from ._models import *

# Put your dependencies here
from .hanoi import Hanoi
from .pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle
from .chairs import Chairs

# Add your puzzle in the puzzleList
puzzleList = {
    Peg.puzzleid: Peg,
    Hanoi.puzzleid: Hanoi,
    Chairs.puzzleid: Chairs
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
