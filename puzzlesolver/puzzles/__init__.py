from ._models import *

# Put your dependencies here
from .hanoi import Hanoi
from .lightsout import LightsOut
from .pegSolitaire import Peg
from .graphpuzzle import GraphPuzzle
from .npuzzle import Npuzzle
from .chairs import Chairs
from .rubiks import Rubiks
from .hopNdrop import HopNDrop

# Add your puzzle in the puzzleList
puzzleList = {
    Npuzzle.puzzleid: Npuzzle,
    Hanoi.puzzleid: Hanoi,
    Chairs.puzzleid: Chairs,
    Rubiks.puzzleid: Rubiks,
    LightsOut.puzzleid: LightsOut,
    Peg.puzzleid: Peg,
    HopNDrop.puzzleid: HopNDrop
}

for puzzle in puzzleList.values():
    if not issubclass(puzzle, ServerPuzzle):
        raise TypeError("Non-ServerPuzzle class found in puzzleList")
