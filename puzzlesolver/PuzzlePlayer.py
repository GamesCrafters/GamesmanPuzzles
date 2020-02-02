from .util import *

class PuzzlePlayer:

    def __init__(self, game, solver=None):
        self.base = game
        self.game = game
        self.solver = solver
        if solver:
            self.solver.solve(self.game)

    # Starts the GameManager
    def play(self):
        self.game = self.base
        while self.game.primitive() == GameValue.UNDECIDED:
            self.printInfo()
            self.printTurn()
        self.printInfo()
        print("Game Over")

    # Prints the game info
    def printInfo(self):
        print("Primitive:     ", self.game.primitive())
        if self.solver:
            print("Solver:        ", self.solver.solve(self.game))
            print("Remoteness:    ", self.solver.getRemoteness(self.game))
        print(str(self.game))

    # Prompts for input and moves
    def printTurn(self):
        moves = self.game.generateMoves()
        print("Possible Moves:", moves)
        print("Enter Piece: ")
        index = int(input())
        if index >= len(moves):
            print("Not a valid move, try again")
        else:
            self.game = self.game.doMove(moves[index])
        print("----------------------------")