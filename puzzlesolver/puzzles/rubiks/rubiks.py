from copy import deepcopy
import random
from .. import ServerPuzzle
from ...util import *
from ...solvers import GeneralSolver, SqliteSolver
# from ..puzzleplayer import PuzzlePlayer

from hashlib import sha1

rot_tile_r = [2,0,3,1]
rot_cube_r = [1,4,2,0,3]
rot_tile_l = [1,3,0,2]
rot_cube_l = [3,0,2,4,1]
rot_tile_2 = [3,2,1,0]
rot_cube_2 = [4,3,2,1,0,5]

class Rubiks(ServerPuzzle):

    id      = 'rubiks'
    auth    = "Mark Presten"
    name    = "Rubik's Cube"
    desc    = """Solve the Rubiks cube by getting one color/number on each face using rotations.."""
    date    = "September 14th, 2020"

    variants = {"2x2" : SqliteSolver}

    def __init__(self, **kwargs):
        #    [0]
        # [1][2][3]
        #    [4]
        #    [5]
        b = [['O',0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]]
        r = random.randint(15, 25)
        moves = ["TopRow->Right", "TopRow->Left", "BottomRow->Right", "BottomRow->Left", "LeftColumn->Up", "LeftColumn->Down", "RightColumn->Up", "RightColumn->Down", "TopTile->Right", "TopTile->Left", "BottomTile->Right", "BottomTile->Left"]
        for i in range(r):
            index = random.randint(0,7)
            move = moves[index]
            if move == "TopRow->Right":
                b = self.topR(b)
            elif move == "TopRow->Left":
                b = self.topL(b)
            elif move == "BottomRow->Right":
                b = self.bottomR(b)
            elif move == "BottomRow->Left":
                b = self.bottomL(b)
            elif move == "LeftColumn->Up":
                b = self.leftUp(b)       
            elif move == "LeftColumn->Down":
                b = self.leftDown(b)  
            elif move == "RightColumn->Up":
                b = self.rightUp(b)  
            elif move == "RightColumn->Down":
                b = self.rightDown(b)
            elif move == "TopTile->Right":
                b = self.topTileRight(b)
            elif move == "TopTile->Left":
                b = self.topTileLeft(b)
            elif move == "BottomTile->Left":
                b = self.bottomTileLeft(b)
            elif move == "BottomTile->Right":
                b = self.bottomTileRight(b)
        self.board = b
        # self.board = [[4, 5, 0, 0], [2, 2, 4, 'O'], [3, 3, 1, 2], [5, 4, 1, 4], [5, 0, 3, 2], [5, 1, 3, 1]]
        # self.board = [[5, 5, 'O', 0], [4, 5, 1, 1], [1, 1, 2, 0], [2, 0, 3, 3], [4, 2, 4, 2], [5, 4, 3, 3]]
        # self.board = [[4, 2, 4, 5], [3, 3, 5, 0], [2, 0, 3, 1], [3, 1, 4, 2], [2, 5, 'O', 0], [1, 1, 5, 4]]


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
        print("Puzzle: ")
        space = "      "
        side = 0
        print(space + "---")
        d = {'O':'O', 0:'O', 1:'B', 2:'G', 3:'W', 4:'R', 5:'Y'}
        while side < 6:
            if side == 0 or side == 4 or side == 5:
                print(space, end="")
                for i in range(4):
                    if i < 2:
                        print(str(d[self.board[side][i]])+ " ", end="")
                    if i == 2:
                        print("")
                        print(space, end="")
                    if i >= 2:
                        print(str(d[self.board[side][i]])+ " ", end="")
                print("")
                print(space + "---")
                side +=1
            else:
                for i in range(2):
                    print(str(d[self.board[side][2*i]])+ " ", end="")
                    print(str(d[self.board[side][2*i+1]])+ " ", end="")
                    print("| ", end="")
                    print(str(d[self.board[side + 1][2*i]])+ " ", end="")
                    print(str(d[self.board[side + 1][2*i+1]])+ " ", end="")
                    print("| ", end="")
                    print(str(d[self.board[side + 2][2*i]])+ " ", end="")
                    print(str(d[self.board[side + 2][2*i+1]])+ " ", end="")
                    print("")
                print(space + "---")
                side = 4
    # ________ End Print Funcs _________

    def getName(self, **kwargs):
        return "Rubik's Cube"

    def playPuzzle(self, moves):
        print("Enter Piece: ")
        d = {"trr":"TopRow->Right", "trl":"TopRow->Left", "brr":"BottomRow->Right", "brl":"BottomRow->Left", "lcu":"LeftColumn->Up", "lcd":"LeftColumn->Down", "rcu":"RightColumn->Up", "rcd":"RightColumn->Down", "ttr":"TopTile->Right", "ttl":"TopTile->Left", "btr":"BottomTile->Right", "btl":"BottomTile->Left"}
        print("| trr -> TopRowRight  | trl -> TopRowLeft    | brr -> BottomRowRight | brl -> BottomRowLeft  |")
        print("| lcu -> LeftColumnUp | lcd -> LeftColumnDown| rcu -> RightColumnUp  | rcd -> RightColumnDown|")
        print("| ttr -> TopTileRight | ttl -> TopTileLeft   | btr -> BottomTileRight| btl -> BottomTileLeft |")
        inp = str(input())
        if inp == '':
            return "BEST"
        elif inp not in d.keys():
            return "OOPS"
        else:
            return d[inp]

    def primitive(self, **kwargs):
        for side in self.board:
            item = side[0]
            if item == 'O':
                item = 0
            for i in side:
                if i == 'O':
                    i = 0
                if i != item:
                    return PuzzleValue.UNDECIDED
        return PuzzleValue.SOLVABLE

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = ["TopRow->Right", "TopRow->Left", "BottomRow->Right", "BottomRow->Left", "LeftColumn->Up", "LeftColumn->Down", "RightColumn->Up", "RightColumn->Down", "TopTile->Right", "TopTile->Left", "BottomTile->Right", "BottomTile->Left"]
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

    def topTileLeft(self, b):
        #2x close components: 0 -> 1,     1 ->  4,   4 ->  3,    3  ->  0
        #                   (3,2) (1,3) (1,3) (0,1) (0,1) (2,0) (2,0)  (3,2)
        new_board = deepcopy(b)
        cells = [0,1,4,3,0]
        d = {0: (3,2), 1: (1,3), 4: (0,1), 3: (2,0)}
        for c in range(4):
            sp_cell = cells[c]
            rot_items = [b[sp_cell][d[sp_cell][0]], b[sp_cell][d[sp_cell][1]]]
            sp_cell_1 = cells[c+1]
            new_board[sp_cell_1][d[sp_cell_1][0]], new_board[sp_cell_1][d[sp_cell_1][1]] = rot_items[0], rot_items[1]
        new_board[2] = [new_board[2][r] for r in rot_tile_l]
        return new_board 

    def topTileRight(self, b):
        #2x close components: 0 -> 3,     3 ->  4,   4 ->  1,    1  ->  0
        #                   (2,3) (0,2) (0,2) (1,0) (1,0) (3,1) (3,1)  (2,3)
        new_board = deepcopy(b)
        cells = [0,3,4,1,0]
        d = {0: (2,3), 3: (0,2), 4: (1,0), 1: (3,1)}
        for c in range(4):
            sp_cell = cells[c]
            rot_items = [b[sp_cell][d[sp_cell][0]], b[sp_cell][d[sp_cell][1]]]
            sp_cell_1 = cells[c+1]
            new_board[sp_cell_1][d[sp_cell_1][0]], new_board[sp_cell_1][d[sp_cell_1][1]] = rot_items[0], rot_items[1]
        new_board[2] = [new_board[2][r] for r in rot_tile_r]
        return new_board 

    def bottomTileLeft(self, b):
        #2x close components: 0 -> 1,     1 ->  4,   4 ->  3,    3  ->  0
        #                   (1,0) (0,2) (0,2) (2,3) (2,3) (3,1) (3,1)  (1,0)
        new_board = deepcopy(b)
        cells = [0,1,4,3,0]
        d = {0: (1,0), 1: (0,2), 4: (2,3), 3: (3,1)}
        for c in range(4):
            sp_cell = cells[c]
            rot_items = [b[sp_cell][d[sp_cell][0]], b[sp_cell][d[sp_cell][1]]]
            sp_cell_1 = cells[c+1]
            new_board[sp_cell_1][d[sp_cell_1][0]], new_board[sp_cell_1][d[sp_cell_1][1]] = rot_items[0], rot_items[1]
        new_board[5] = [new_board[5][r] for r in rot_tile_r]
        return new_board 

    def bottomTileRight(self, b):
        #2x close components: 0 -> 3,     3 ->  4,   4 ->  1,    1  ->  0
        #                   (0,1) (1,3) (1,3) (3,2) (3,2) (2,0) (2,0)  (0,1)
        new_board = deepcopy(b)
        cells = [0,3,4,1,0]
        d = {0: (0,1), 3: (1,3), 4: (3,2), 1: (2,0)}
        for c in range(4):
            sp_cell = cells[c]
            rot_items = [b[sp_cell][d[sp_cell][0]], b[sp_cell][d[sp_cell][1]]]
            sp_cell_1 = cells[c+1]
            new_board[sp_cell_1][d[sp_cell_1][0]], new_board[sp_cell_1][d[sp_cell_1][1]] = rot_items[0], rot_items[1]
        new_board[5] = [new_board[5][r] for r in rot_tile_l]
        return new_board 

    ### _________ end HELPERS _________________ ###

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError
        newPuzzle = Rubiks()
        if move == "TopRow->Right":
            new_board = self.topR(self.board)
        elif move == "TopRow->Left":
            new_board = self.topL(self.board)
        elif move == "BottomRow->Right":
            new_board = self.bottomR(self.board)
        elif move == "BottomRow->Left":
            new_board = self.bottomL(self.board)
        elif move == "LeftColumn->Up":
            new_board = self.leftUp(self.board)       
        elif move == "LeftColumn->Down":
            new_board = self.leftDown(self.board)  
        elif move == "RightColumn->Up":
            new_board = self.rightUp(self.board)  
        elif move == "RightColumn->Down":
            new_board = self.rightDown(self.board)  
        elif move == "TopTile->Right":
            new_board = self.topTileRight(self.board)
        elif move == "TopTile->Left":
            new_board = self.topTileLeft(self.board)
        elif move == "BottomTile->Right":
            new_board = self.bottomTileRight(self.board)
        elif move == "BottomTile->Left":
            new_board = self.bottomTileLeft(self.board)
        newPuzzle.board = new_board
        return newPuzzle   

    ### ____________ Solver Funcs ________________


    ### ___ HASH ____ ###
    def center_cube(self, board):
        #Find which tile contains 'O'
        ind = [('O' in x) for x in board].index(True)
        #Get this tile to the center
        if ind == 0:
            #rotate left->down & right->down
            board = self.leftDown(board)
            board = self.rightDown(board)
        elif ind == 1:
            # rotate top->right & bottom-> right
            board = self.topR(board)
            board = self.bottomR(board)
        elif ind == 2:
            temp = 0 #Nothing
        elif ind == 3:
            # rotate top->left & bottom-> left
            board = self.topL(board)
            board = self.bottomL(board)
        elif ind == 4:
            #rotate left->up & right->up
            board = self.leftUp(board)
            board = self.rightUp(board)
        else:
            #rotate left->up x2 & right->up x2
            board = self.leftUp(board)
            board = self.rightUp(board)
            board = self.leftUp(board)
            board = self.rightUp(board)
        #Rotate tile s.t. 'O' in top left
        ind = board[2].index('O')
        if ind == 0:
            # print("Nothing")
            new_board = board
        elif ind == 1:
            #rotate left
            new_board = [[board[x][r] for r in rot_tile_l] for x in range(5)]
            new_board = [new_board[r] for r in rot_cube_l]
            new_board.append([board[5][r] for r in rot_tile_r])
        elif ind == 2:
            #rotate right
            new_board = [[board[x][r] for r in rot_tile_r] for x in range(5)]
            new_board = [new_board[r] for r in rot_cube_r]
            new_board.append([board[5][r] for r in rot_tile_l])
        else:
            #rotate right x2
            new_board = [[board[x][r] for r in rot_tile_2] for x in range(6)]
            new_board = [new_board[r] for r in rot_cube_2]
        return new_board

    def __hash__(self):
        h = sha1()
        b = self.center_cube(self.board)
        h.update(str(b).encode())
        return int(h.hexdigest(), 16)

    ### _____ END HASH ________ ###
        

    def generateSolutions(self, **kwargs):
        newPuzzle1 = Rubiks()
        newPuzzle1.board = [['O',0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]]
        # newPuzzle2 = Rubiks()
        # newPuzzle2.board = [[5,5,5,5],[1,1,1,1],['O',0,0,0],[3,3,3,3],[2,2,2,2],[4,4,4,4]]
        # newPuzzle3 = Rubiks()
        # newPuzzle3.board = [[4,4,4,4],[1,1,1,1],[5,5,5,5],[3,3,3,3],['O',0,0,0],[2,2,2,2]]
        # newPuzzle4 = Rubiks()
        # newPuzzle4.board = [[2,2,2,2],[1,1,1,1],[4,4,4,4],[3,3,3,3],[5,5,5,5],['O',0,0,0]]
        # newPuzzle5 = Rubiks()
        # newPuzzle5.board = [['O',0,0,0],[5,5,5,5],[1,1,1,1],[2,2,2,2],[4,4,4,4],[3,3,3,3]]
        # newPuzzle6 = Rubiks()
        # newPuzzle6.board = [['O',0,0,0],[2,2,2,2],[3,3,3,3],[5,5,5,5],[4,4,4,4],[1,1,1,1]]
        # return [newPuzzle1,newPuzzle2, newPuzzle3, newPuzzle4, newPuzzle5, newPuzzle6]
        return [newPuzzle1]

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
            elif i == "O":
                new_panel.append(i)
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
        puzzle = cls.deserialize(positionid)
        for i in range(6):
            if len(puzzle.board[i]) != 4:
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
        b = [['O',0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5]]
        r = random.randint(15, 25)
        r = 15
        moves = ["TopRow->Right", "TopRow->Left", "BottomRow->Right", "BottomRow->Left", "LeftColumn->Up", "LeftColumn->Down", "RightColumn->Up", "RightColumn->Down", "TopTile->Right", "TopTile->Left", "BottomTile->Right", "BottomTile->Left"]
        for i in range(r):
            index = random.randint(0,7)
            move = moves[index]
            if move == "TopRow->Right":
                b = cls.topR(cls, b)
            elif move == "TopRow->Left":
                b = cls.topL(cls, b)
            elif move == "BottomRow->Right":
                b = cls.bottomR(cls, b)
            elif move == "BottomRow->Left":
                b = cls.bottomL(cls, b)
            elif move == "LeftColumn->Up":
                b = cls.leftUp(cls, b)       
            elif move == "LeftColumn->Down":
                b = cls.leftDown(cls, b)  
            elif move == "RightColumn->Up":
                b = cls.rightUp(cls, b)  
            elif move == "RightColumn->Down":
                b = cls.rightDown(cls, b)
            elif move == "TopTile->Right":
                b = cls.topTileRight(cls, b)
            elif move == "TopTile->Left":
                b = cls.topTileLeft(cls, b)
            elif move == "BottomTile->Left":
                b = cls.bottomTileLeft(cls, b)
            elif move == "BottomTile->Right":
                b = cls.bottomTileRight(cls, b)
        puzzle = Rubiks()
        puzzle.board = b
        return puzzle    

# if __name__ == "__main__":
#     puzzle = Rubiks()
#     PuzzlePlayer(puzzle, SqliteSolver(puzzle=puzzle), bestmove=True, auto=False).play()

