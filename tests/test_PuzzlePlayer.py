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
    p2.setMove(p3, movetype="for")
    p3.setMove(p4, movetype="for")

    s = GeneralSolver(p1)
    pp = PuzzlePlayer(p1, s)

    input_mock = mock.Mock(return_value=0)

    with mock.patch('puzzlesolver.puzzleplayer.input', input_mock):
        pp.play()
    assert input_mock.call_count == 3