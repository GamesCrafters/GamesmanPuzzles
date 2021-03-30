import pytest
from unittest import mock

from puzzlesolver.players.tui import TUI
from puzzlesolver.puzzles.graphpuzzle import GraphPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.util import *

@pytest.mark.skip(reason="Wait until a future implementation")
def testBestMove():
    p1 = GraphPuzzle("0", value=PuzzleValue.UNDECIDED)
    p2 = GraphPuzzle("1", value=PuzzleValue.UNDECIDED)
    p3 = GraphPuzzle("2", value=PuzzleValue.UNDECIDED)
    p4 = GraphPuzzle("3", value=PuzzleValue.SOLVABLE)

    p1.setMove(p2, movetype="for")
    p2.setMove(p3, movetype="for")
    p3.setMove(p4, movetype="for")

    solver = GeneralSolver(p1)
    player = TUI(p1, solver, debug=True)

    input_mock = mock.Mock(return_value=0)

    with mock.patch('puzzlesolver.players.tui.input', input_mock):
        player.play()
    assert input_mock.call_count == 3
