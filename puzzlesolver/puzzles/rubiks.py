from copy import deepcopy
import random
from . import ServerPuzzle
from ..util import *
from ..solvers import GeneralSolver, SqliteSolver
from ..puzzleplayer import PuzzlePlayer

from hashlib import sha1

class Rubiks(ServerPuzzle):

    puzzleid = 'rubiks'
    author = "Mark Presten"
    puzzle_name = "Rubik's Cube"
    description = """Solve the Rubiks cube by getting one color/number on each face using rotations.."""
    date_created = "September 14th, 2020"

    variants = {"2x2" : SqliteSolver}

    def __init__(self, **kwargs):
        #    [0]
        # [1][2][3]
        #    [4]
        #    [5]
        self.board = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]]
        # self.board = [[0,0,0,0],[2,2,1,1],[3,3,2,2],[5,5,3,3],[4,4,4,4],[5,5,1,1]]


    def __str__(self, **kwargs):
        return str(self.board)

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself.
        Example: '5x5', '3x4', 'reverse3x3'
        """
        return "2x2"

    ### _________ Print Funcs _______________
    def printInfo(self):
        space = "      "
        side = 0
        print(space + "---")
        while side < 6:
            if side == 0 or side == 4 or side == 5:
                print(space, end="")
                for i in range(4):
                    if i < 2:
                        print(str(self.board[side][i])+ " ", end="")
                    if i == 2:
                        print("")
                        print(space, end="")
                    if i >= 2:
                        print(str(self.board[side][i])+ " ", end="")
                print("")
                print(space + "---")
                side +=1
            else:
                for i in range(2):
                    print(str(self.board[side][2*i])+ " ", end="")
                    print(str(self.board[side][2*i+1])+ " ", end="")
                    print("| ", end="")
                    print(str(self.board[side + 1][2*i])+ " ", end="")
                    print(str(self.board[side + 1][2*i+1])+ " ", end="")
                    print("| ", end="")
                    print(str(self.board[side + 2][2*i])+ " ", end="")
                    print(str(self.board[side + 2][2*i+1])+ " ", end="")
                    print("")
                print(space + "---")
                side = 4

    def getName(self, **kwargs):
        return "Rubik's Cube"
    # ________ End Print Funcs _________

    def primitive(self, **kwargs):
        for side in self.board:
            item = side[0]
            for i in side:
                if i != item:
                    return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = ["Top->Right", "Top->Left", "Bottom->Right", "Bottom->Left", "Left->Up", "Left->Down", "Right->Up", "Right->Down"]
        if movetype=='bi' or movetype=='legal' or movetype=='all' or movetype=='undo':
            return moves
        elif movetype=='for' or movetype=='back':
            return []

    ### _____ doMove HELPERS _______ ###

    #    [0]
    # [1][2][3]
    #    [4]
    #    [5]
    def topR(self, b):
        # 1->2, 2->3, 3->5, 5->1
        new_board = deepcopy(b)
        cells = [1,2,3,5,1]
        for c in range(4):
            if cells[c] == 3:
                rot_items = b[cells[c]][:2]
                new_board[cells[c+1]][2:4] = rot_items[::-1]
            elif cells[c] == 5:
                rot_items = b[cells[c]][2:4][::-1]
                new_board[cells[c+1]][:2] = rot_items
            else:
                rot_items = b[cells[c]][:2]
                new_board[cells[c+1]][:2] = rot_items
        #rotate panel 0
        new_board[0] = [b[0][1], b[0][3], b[0][0], b[0][2]]
        return new_board

    def bottomR(self, b):
        # 1->2, 2->3, 3->5, 5->1
        new_board = deepcopy(b)
        cells = [1,2,3,5,1]
        for c in range(4): 
            if cells[c] == 3:
                rot_items = b[cells[c]][2:4]
                new_board[cells[c+1]][:2] = rot_items[::-1]
            elif cells[c] == 5:
                rot_items = b[cells[c]][:2][::-1]
                new_board[cells[c+1]][2:4] = rot_items
            else:
                rot_items = b[cells[c]][2:4]
                new_board[cells[c+1]][2:4] = rot_items
        #rotate panel 4
        new_board[4] = [b[4][2], b[4][0], b[4][3], b[4][1]]
        return new_board

    def topL(self, b):
        # 3->2, 2->1, 1->5, 5->3
        new_board = deepcopy(b)
        cells = [3,2,1,5,3]
        for c in range(4):
            if cells[c] == 1:
                rot_items = b[cells[c]][:2]
                new_board[cells[c+1]][2:4] = rot_items[::-1]
            elif cells[c] == 5:
                rot_items = b[cells[c]][2:4][::-1]
                new_board[cells[c+1]][:2] = rot_items
            else:
                rot_items = b[cells[c]][:2]
                new_board[cells[c+1]][:2] = rot_items
        #rotate panel 0
        new_board[0] = [b[0][2], b[0][0], b[0][3], b[0][1]]
        return new_board

    def bottomL(self, b):
        # 3->2, 2->1, 1->5, 5->3
        new_board = deepcopy(b)
        cells = [3,2,1,5,3]
        for c in range(4):
            if cells[c] == 1:
                rot_items = b[cells[c]][2:4]
                new_board[cells[c+1]][:2] = rot_items[::-1]
            elif cells[c] == 5:
                rot_items = b[cells[c]][:2][::-1]
                new_board[cells[c+1]][2:4] = rot_items
            else:
                rot_items = b[cells[c]][2:4]
                new_board[cells[c+1]][2:4] = rot_items
        #rotate panel 4
        new_board[4] = [b[4][1], b[4][3], b[4][0], b[4][2]]
        return new_board

    def leftUp(self, b):
        #5->4, 4->2, 2->0, 0->5
        new_board = deepcopy(b)
        cells = [5,4,2,0,5]
        for c in range(4):
            rot_items = [b[cells[c]][0], b[cells[c]][2]]
            new_board[cells[c+1]][0], new_board[cells[c+1]][2] = rot_items[0], rot_items[1]
        #rotate panel 1
        new_board[1] = [b[1][1], b[1][3], b[1][0], b[1][2]]
        return new_board  

    def leftDown(self, b):
        #0->2, 2->4, 4->5, 5->0
        new_board = deepcopy(b)
        cells = [0,2,4,5,0]
        for c in range(4):
            rot_items = [b[cells[c]][0], b[cells[c]][2]]
            new_board[cells[c+1]][0], new_board[cells[c+1]][2] = rot_items[0], rot_items[1]
        #rotate panel 1
        new_board[1] = [b[1][2], b[1][0], b[1][3], b[1][1]]
        return new_board  

    def rightUp(self, b):
        #5->4, 4->2, 2->0, 0->5
        new_board = deepcopy(b)
        cells = [5,4,2,0,5]
        for c in range(4):
            rot_items = [b[cells[c]][1], b[cells[c]][3]]
            new_board[cells[c+1]][1], new_board[cells[c+1]][3] = rot_items[0], rot_items[1]
        #rotate panel 3
        new_board[3] = [b[3][2], b[3][0], b[3][3], b[3][1]]
        return new_board 

    def rightDown(self, b):
        #0->2, 2->4, 4->5, 5->0
        new_board = deepcopy(b)
        cells = [0,2,4,5,0]
        for c in range(4):
            rot_items = [b[cells[c]][1], b[cells[c]][3]]
            new_board[cells[c+1]][1], new_board[cells[c+1]][3] = rot_items[0], rot_items[1]
        #rotate panel 3
        new_board[3] = [b[3][1], b[3][3], b[3][0], b[3][2]]
        return new_board 

    ### _________ end HELPERS _________________ ###

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = Rubiks()
        if move == "Top->Right":
            new_board = self.topR(self.board)
        elif move == "Top->Left":
            new_board = self.topL(self.board)
        elif move == "Bottom->Right":
            new_board = self.bottomR(self.board)
        elif move == "Bottom->Left":
            new_board = self.bottomL(self.board)
        elif move == "Left->Up":
            new_board = self.leftUp(self.board)       
        elif move == "Left->Down":
            new_board = self.leftDown(self.board)  
        elif move == "Right->Up":
            new_board = self.rightUp(self.board)  
        elif move == "Right->Down":
            new_board = self.rightDown(self.board)  

        newPuzzle.board = new_board
        return newPuzzle   

    ### ____________ Solver Funcs ________________

    def __hash__(self):
        h = sha1()
        h.update(str(self.board).encode())
        return int(h.hexdigest(), 16)
        
        

    def generateSolutions(self, **kwargs):
        newPuzzle1 = Rubiks()
        newPuzzle1.board = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]]
        newPuzzle2 = Rubiks()
        newPuzzle2.board = [[5,5,5,5],[1,1,1,1],[0,0,0,0],[3,3,3,3],[2,2,2,2],[4,4,4,4]]
        newPuzzle3 = Rubiks()
        newPuzzle3.board = [[4,4,4,4],[1,1,1,1],[5,5,5,5],[3,3,3,3],[0,0,0,0],[2,2,2,2]]
        newPuzzle4 = Rubiks()
        newPuzzle4.board = [[2,2,2,2],[1,1,1,1],[4,4,4,4],[3,3,3,3],[5,5,5,5],[0,0,0,0]]
        newPuzzle5 = Rubiks()
        newPuzzle5.board = [[0,0,0,0],[5,5,5,5],[1,1,1,1],[2,2,2,2],[4,4,4,4],[3,3,3,3]]
        newPuzzle6 = Rubiks()
        newPuzzle6.board = [[0,0,0,0],[2,2,2,2],[3,3,3,3],[5,5,5,5],[4,4,4,4],[1,1,1,1]]
        return [newPuzzle1,newPuzzle2, newPuzzle3, newPuzzle4, newPuzzle5, newPuzzle6]

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
        puzzle = Rubiks()
        out = []
        new_panel = []
        for i in positionid:
            if i == "-":
                out.append(new_panel)
                new_panel = []
            else:
                new_panel.append(int(i))
        out.append(new_panel)
        puzzle.board = out
        return puzzle

    def serialize(self, **kwargs):
        """Returns a serialized based on self
        Outputs:
            String Puzzle
        """
        out = ""
        for panel in range(len(self.board)):
            for i in self.board[panel]:
                out += str(i)
            if panel == len(self.board)-1:
                break
            out += "-"
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
        for i in range(6):
            if len(self.board[i]) != 4:
                return False
        return True

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Rubiks.variants: raise IndexError("Out of bounds variantid")
        b = [[0,0,0,0],[2,2,1,1],[3,3,2,2],[5,5,3,3],[4,4,4,4],[5,5,1,1]]
        # b = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]]
        # r = random.randint(15, 25)
        # r = 1
        # moves = ["Top->Right", "Top->Left", "Bottom->Right", "Bottom->Left", "Left->Up", "Left->Down", "Right->Up", "Right->Down"]
        # for i in range(r):
        #     index = random.randint(0,7)
        #     move = moves[index]
        #     if move == "Top->Right":
        #         b = self.topR(b)
        #     elif move == "Top->Left":
        #         b = self.topL(b)
        #     elif move == "Bottom->Right":
        #         b = self.bottomR(b)
        #     elif move == "Bottom->Left":
        #         b = self.bottomL(b)
        #     elif move == "Left->Up":
        #         b = self.leftUp(b)       
        #     elif move == "Left->Down":
        #         b = self.leftDown(b)  
        #     elif move == "Right->Up":
        #         b = self.rightUp(b)  
        #     elif move == "Right->Down":
        #         b = self.rightDown(b)
        puzzle = Rubiks()
        puzzle.board = b
        return puzzle    

if __name__ == "__main__":
    puzzle = Rubiks()
    PuzzlePlayer(puzzle, GeneralSolver(puzzle=puzzle), bestmove=True, auto=False).play()

# PuzzlePlayer(Chairs(), solver=GeneralSolver(), auto=True).play()
# PuzzlePlayer(Peg()).play()