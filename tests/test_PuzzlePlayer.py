import pytest
from unittest import mock

from puzzlesolver.puzzleplayer import PuzzlePlayer
from puzzlesolver.puzzles.graphpuzzle import GraphPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

def testGeneral():
    p1 = GraphPuzzle("0", value=PuzzleValue.UNDECIDED)
    p2 = GraphPuzzle("1", value=PuzzleValue.UNDECIDED)
    p3 = GraphPuzzle("2", value=PuzzleValue.UNDECIDED)
    p4 = GraphPuzzle("3", value=PuzzleValue.SOLVABLE)

    p1.setMove(p2, movetype="for")
    p2.setMove(p3, movetype="bi")
    p3.setMove(p4, movetype="for")

    s = GeneralSolver(p1)
    pp = PuzzlePlayer(p1, s)