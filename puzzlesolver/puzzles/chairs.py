from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import SqliteSolver

from hashlib import sha1

class Chairs(ServerPuzzle):

    puzzleid = 'chairs'
    author = "Mark Presten"
    name = "Chair Hopping"
    description = """Move all pieces from one side of the board to the other by hopping over adjacent pieces. The end result should be a flipped version of the starting state."""
    date_created = "April 25, 2020"

    variants = {"10" : SqliteSolver}
    test_variants = variants

    def __init__(self, **kwargs):
        self.board = ['x','x','x','x','x', '-', 'o','o','o','o','o']

    def __str__(self, **kwargs):
        return str(self.board)

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself.
        Example: '5x5', '3x4', 'reverse3x3'
        """
        return "10"

    ### _________ Print Funcs _______________
    def printInfo(self):
        #Print Puzzle
        output = ""
        space = "   "
        output += space
        for i in self.board:
            if i == "-":
                i = "_"
            output += i + "   "
        output += "\n"
        space = "  ["
        output += space
        for i in range(11):
            if i == 10:
                output += str(i) + "]"
                break
            output += str(i) + "   "
        output += "\n"
        return output

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
        h = sha1()
        h.update(str(self.board).encode())
        return int(h.hexdigest(), 16)

    def generateSolutions(self, **kwargs):
        newPuzzle = Chairs()
        newPuzzle.board = ['o','o','o','o','o','-','x','x','x','x','x']
        return [newPuzzle]

    ### ________ Server _________
    @classmethod
    def deserialize(cls, positionid, **kwargs):
        """Returns a Puzzle object based on positionid
        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))
        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it
        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        puzzle = Chairs()
        out = []
        for i in positionid:
            out.append(i)
        puzzle.board = out
        return puzzle

    def serialize(self, **kwargs):
        """Returns a serialized based on self
        Outputs:
            String Puzzle
        """
        out = ""
        for i in self.board:
            out += i
        return out

    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        """Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified
        For example, Hanoi cannot have a larger ring on top of a smaller one.
        Outputs:
            - True if Puzzle is valid, else False
        """
        try: puzzle = cls.deserialize(positionid)
        except: raise PuzzleException("Position is invalid")
        xcount = 0
        ocount = 0
        dcount = 0
        for i in puzzle.board:
            if i == 'x':
                xcount += 1
            elif i == 'o':
                ocount += 1
            elif i == '-':
                dcount += 1
        if xcount != ocount or xcount != 5 or dcount != 1:
            return False
        return True

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Chairs.variants: raise IndexError("Out of bounds variantid")
        return Chairs()