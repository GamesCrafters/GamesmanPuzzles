"""
This class provides a CLI for interaction with Solvers and Puzzles
"""
from .util import *

class PuzzlePlayer:

    def __init__(self, puzzle, solver=None, auto=False):
        self.base = puzzle
        self.puzzle = puzzle
        self.solver = solver
        self.auto = auto
        if solver:
            self.solver.solve(self.puzzle)

    # Starts the PuzzlePlayer
    def play(self):
        self.puzzle = self.base
        self.turn = 0
        while self.puzzle.primitive() == PuzzleValue.UNDECIDED:
            self.printInfo()
            self.printTurn()
        self.printInfo()
        print("Game Over")

    # Prints the puzzle info
    def printInfo(self):
        print("Turn:          ", self.turn), 
        print("Primitive:     ", self.puzzle.primitive())
        if self.solver:
            print("Solver:        ", self.solver.solve(self.puzzle))
            print("Remoteness:    ", self.solver.getRemoteness(self.puzzle))
        print(str(self.puzzle))
        self.turn += 1

    # Prompts for input and moves
    def printTurn(self):
        if self.auto: 
            move = self.generateBestMove()
            self.puzzle = self.puzzle.doMove(move)
        else:
            moves = self.puzzle.generateLegalMoves()
            print("Possible Moves:", moves)
            print("Enter Piece: ")
            index = int(input())
            if index >= len(moves):
                print("Not a valid move, try again")
            else:
                self.puzzle = self.puzzle.doMove(moves[index])
        print("----------------------------")

    def generateBestMove(self):
        remotes = {
            self.solver.getRemoteness(self.puzzle.doMove(move)) : move 
            for move in self.puzzle.generateLegalMoves()
        }
        return remotes[min(remotes.keys())]

