"""
This class provides a TUI for interaction with Solvers and Puzzles
"""
from .util import *

#Default to print Puzzle Info
def printPuzzle(puzzle):
    print(str(puzzle))

class PuzzlePlayer:

    def __init__(self, puzzle, solver=None, auto=False, printPuzzleInfo=printPuzzle):
        self.base = puzzle
        self.puzzle = puzzle
        self.solver = solver
        self.auto = auto
        self.printPuzzle = printPuzzleInfo
        if solver:
            self.solver.solve(self.puzzle)

    # Starts the PuzzlePlayer
    def play(self):
        self.puzzle = self.base
        self.turn = 0
        while self.puzzle.primitive() == PuzzleValue.UNDECIDED:
            self.printInfo()
            self.printPuzzle(self.puzzle)
            self.printTurn()
        self.printInfo()
        self.printPuzzle(self.puzzle)
        print("Game Over")

    def printInfo(self):
        print("Turn:          ", self.turn), 
        print("Primitive:     ", self.puzzle.primitive())
        if self.solver:
            print("Solver:        ", self.solver.solve(self.puzzle))
            print("Remoteness:    ", self.solver.getRemoteness(self.puzzle))
        self.turn += 1

    # Prompts for input and moves
    def printTurn(self):
        if self.auto: 
            move = self.generateBestMove()
            self.puzzle = self.puzzle.doMove(move)
        else:
            moves = self.puzzle.generateMoves(movetype="legal")
            print("Possible Moves:")
            for count, m in enumerate(moves):
                print(str(count) + " -> " + str(m))
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

