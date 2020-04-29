from copy import deepcopy
from . import Puzzle
from ..util import *
from ..solvers import GeneralSolver
from ..puzzleplayer import PuzzlePlayer


class Chairs(Puzzle):
    def __init__(self, **kwargs):
        self.board = ['x','x','x','x','x', '-', 'o','o','o','o','o']

    def __str__(self, **kwargs):
        return str(self.board)

    ### _________ Print Funcs _______________
    def printInfo(self):
        #Print Puzzle
        print("Puzzle: ")
        space = "   "
        print(space, end="")
        for i in self.board:
            if i == "-":
                i = "_"
            print(i + "   ", end="")
        print("")
        space = "  ["
        print(space, end="")
        for i in range(11):
            if i == 10:
                print(str(i) + "]", end="")
                break
            print(str(i) + "   ", end="")
        print("")

    def getName(self, **kwargs):
        return "Chairs"
    # ________ End Print Funcs _________

    def primitive(self, **kwargs):
        if self.board == ['o','o','o','o','o','-','x','x','x','x','x']:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = []
        key = False
        if movetype=='bi':
            return []
        if movetype=='all':
            key = True
        if movetype=='for' or movetype=='legal' or key:
            moves.extend(self.xForward())
            moves.extend(self.oForward())
        if movetype=='undo' or movetype=='back' or key:
            moves.extend(self.xBack())
            moves.extend(self.oBack())
        return moves

    ### _____ generateMoves HELPERS _______ ###

    def xForward(self):
        moves = []
        for count, ele in enumerate(self.board):
            if ele == '-' and count > 0:
                if self.board[count - 1] == 'x':
                    moves.append(count - 1)
                if count > 1:
                    if self.board[count - 2] == 'x':
                        moves.append(count - 2)
        return moves

    def xBack(self):
        moves = []
        for count, ele in enumerate(self.board):
            if ele == '-' and count < 10:
                if self.board[count + 1] == 'x':
                    moves.append(count + 1)
                if count < 9:
                    if self.board[count + 2] == 'x':
                        moves.append(count + 2)
        return moves            

    def oForward(self):
        moves = []
        for count, ele in enumerate(self.board):
            if ele == '-' and count < 10:
                if self.board[count + 1] == 'o':
                    moves.append(count + 1)
                if count < 9:
                    if self.board[count + 2] == 'o':
                        moves.append(count + 2)
        return moves

    def oBack(self):
        moves = []
        for count, ele in enumerate(self.board):
            if ele == '-' and count > 0:
                if self.board[count - 1] == 'o':
                    moves.append(count - 1)
                if count > 1:
                    if self.board[count - 2] == 'o':
                        moves.append(count - 2)
        return moves

    ### _________ end HELPERS _________________ ###

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = Chairs()
        new_board = deepcopy(self.board)
        ind = new_board.index('-')
        ele = new_board[move]
        new_board[move] = '-'
        new_board[ind] = ele
        newPuzzle.board = new_board
        return newPuzzle   

    ### ____________ Solver Funcs ________________

    def __hash__(self):
        return hash(str(self.board))

    def generateSolutions(self, **kwargs):
        newPuzzle = Chairs()
        newPuzzle.board = ['o','o','o','o','o','-','x','x','x','x','x']
        return [newPuzzle]

# PuzzlePlayer(Chairs(), solver=GeneralSolver(), auto=True).play()
# PuzzlePlayer(Peg()).play()

