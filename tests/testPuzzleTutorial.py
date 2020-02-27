import pytest

from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles.puzzle import Puzzle
from puzzlesolver.solvers.generalsolver import GeneralSolver
from puzzlesolver.puzzleplayer import PuzzlePlayer

class Hanoi(Puzzle):
    def __init__(self):
        self.stacks = [[3, 2, 1], [], []]

    def __str__(self):
        return str(self.stacks)

    def primitive(self):
        if self.stacks[2] == [3, 2, 1]:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self):
        moves = []
        for i, stack1 in enumerate(self.stacks):
            if not stack1: continue
            for j, stack2 in enumerate(self.stacks):
                if i == j: continue
                if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
        return moves

    def doMove(self, move):
        newPuzzle = Hanoi()
        stacks = deepcopy(self.stacks)
        stacks[move[1]].append(stacks[move[0]].pop())
        newPuzzle.stacks = stacks
        return newPuzzle

    def __hash__(self):
        return hash(str(self.stacks))

    def generateSolutions(self):
        newPuzzle = Hanoi()
        newPuzzle.stacks = [
            [],
            [],
            [3, 2, 1]
        ]
        return [newPuzzle]

def testTutorial():
    puzzle = Hanoi()
    solver = GeneralSolver()
    solver.solve(puzzle)
    assert solver.getRemoteness(puzzle) == 7