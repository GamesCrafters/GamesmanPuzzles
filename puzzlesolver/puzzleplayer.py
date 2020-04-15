"""
This class provides a TUI for interaction with Solvers and Puzzles
"""
from .util import *

class PuzzlePlayer:

    def __init__(self, puzzle, solver=None, auto=False):
        self.base = puzzle
        self.puzzle = puzzle
        self.solver = solver
        self.auto = auto
        if solver:
            self.solver.solve()

    # Starts the PuzzlePlayer
    def play(self):
        self.puzzle = self.base
        self.turn = 0
        while self.puzzle.primitive() == PuzzleValue.UNDECIDED:
            self.printInfo()
            self.puzzle.printInfo()
            self.printTurn()
        self.printInfo()
        self.puzzle.printInfo()
        print("Game Over")

    def printInfo(self):
        print("Turn:          ", self.turn), 
        print("Primitive:     ", self.puzzle.primitive())
        if self.solver:
            print("Solver:        ", self.solver.getValue(self.puzzle))
            print("Remoteness:    ", self.solver.getRemoteness(self.puzzle))
        self.turn += 1

    # Prompts for input and moves
    def printTurn(self):
        if self.auto: 
            move = self.generateBestMove()
            self.puzzle = self.puzzle.doMove(move)
        else:
<<<<<<< HEAD
            moves = self.puzzle.generateMoves(movetype="legal")
            print("Possible Moves:")
            for count, m in enumerate(moves):
                print("(" + str(count) + ") -> " + str(m))
=======
            moves = list(self.puzzle.generateMoves(movetype="legal"))
            print("Possible Moves:", moves)
>>>>>>> d666e340aa815ce8aa6084d734f812e419458108
            print("Enter Piece: ")
            index = int(input())
            if index >= len(moves):
                print("Not a valid move, try again")
            else:
                self.puzzle = self.puzzle.doMove(moves[index])
        print("----------------------------")

    # Generates best move from the solver
    def generateBestMove(self):
        remotes = {
            self.solver.getRemoteness(self.puzzle.doMove(move)) : move 
            for move in self.puzzle.generateMoves(movetype="legal")
        }
        if PuzzleValue.UNSOLVABLE in remotes:
            del remotes[PuzzleValue.UNSOLVABLE]
        return remotes[min(remotes.keys())]

