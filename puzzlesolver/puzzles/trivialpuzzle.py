from copy import deepcopy
from .Puzzle import Puzzle
from ..util import *
from ..solver.GeneralSolver import GeneralSolver
from ..PuzzlePlayer import PuzzlePlayer
import numpy as np

class TrivialPuzzle(Puzzle):
    
    def __init__(self, size=3):
        self.board = np.zeros(size**2).reshape(size,size)
        self.board[0,0] = 1
        self.board[2,0] = 1
        self.size = size

    def primitive(self):
        if np.sum(self.board) == 1:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def doMove(self, move):
        assert len(move) == 2, "Not a valid move"
        puzzle = TrivialPuzzle()
        puzzle.board = deepcopy(self.board)
        start, finish = move[0], move[1]
        if self.board[start] == 1 and self.board[finish] == 1:
            puzzle.board[start] = 0
        elif self.board[start] == 1 and self.board[finish] == 0:
            puzzle.board[finish] = 1
        else:
            print(move)
            print(self.board[start])
            raise ValueError
        return puzzle
    
    def validIndex(self, pos):
        return pos[0] < self.size and pos[0] >= 0 and pos[1] < self.size and pos[1] >= 0

    def generateHelperMoves(self, undo=False):
        validFinish = 0 if undo else 1
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                piece, pos = self.board[i, j], (i, j)
                if piece == 0: continue
                finishes = [(pos[0] + 1, pos[1]),
                            (pos[0] - 1, pos[1]),
                            (pos[0], pos[1] + 1),
                            (pos[0], pos[1] - 1)]
                moves += [(pos, i) for i in finishes if self.validIndex(i) and self.board[i] == validFinish]
        return moves

    def generateMoves(self, move_type="legal"):
        if move_type == "legal":
            return self.generateHelperMoves()
        return self.generateHelperMoves(undo=True)
    
    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        return str(self.board)

    def generateSolutions(self):
        board = np.zeros(self.size**2)
        solutions = []
        for i in range(len(board)):
            boardcopy = deepcopy(board)
            boardcopy[i] = 1
            puzzle = TrivialPuzzle()
            puzzle.board = boardcopy.reshape(self.size, self.size)
            solutions.append(puzzle)
        return solutions

if __name__ == "__main__":   
    PuzzlePlayer(TrivialPuzzle(), GeneralSolver()).play()