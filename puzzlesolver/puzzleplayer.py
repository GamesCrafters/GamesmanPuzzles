"""
This class provides a TUI for interaction with Solvers and Puzzles
"""
from .util import *

class PuzzlePlayer:

    def __init__(self, puzzle, solver=None, solverinfo=True, auto=False, bestmove=False):
        self.base = puzzle
        self.puzzle = puzzle
        self.solver = solver
        self.solverinfo = solverinfo
        self.auto = auto
        self.bestmove = bestmove
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
        if self.solverinfo and self.solver:
            print("Solver:        ", self.solver.getValue(self.puzzle))
            print("Remoteness:    ", self.solver.getRemoteness(self.puzzle))
        if self.bestmove: print("Best Move:     ", self.generateBestMove())
        self.turn += 1

    # Prompts for input and moves
    def printTurn(self):
        move = self.generateBestMove()
        # Auto generate a possible solution
        if self.auto: self.puzzle = self.puzzle.doMove(move)
        else:
            moves = list(self.puzzle.generateMoves(movetype="legal"))
            # Have the best move be the first index
            if self.bestmove: 
                moves.remove(move)
                moves.insert(0, move)
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
        if self.solver.getValue(self.puzzle) == PuzzleValue.UNSOLVABLE: return None
        if self.puzzle.primitive() == PuzzleValue.SOLVABLE: return None
        remotes = {
            self.solver.getRemoteness(self.puzzle.doMove(move)) : move 
            for move in self.puzzle.generateMoves(movetype="legal")
        }
        if PuzzleValue.UNSOLVABLE in remotes:
            del remotes[PuzzleValue.UNSOLVABLE]
        return remotes[min(remotes.keys())]