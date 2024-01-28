"""
File: hopNdrop.py
Puzzle: Towers of Hanoi
Author: Mark Presten
Date: Oct 10, 2020
"""

"""
    (STILL IN DEVELOPMENT)
    Some sections of code commented out until someone 
    can fix the AutoGUI.
"""

from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import GeneralSolver, SqliteSolver
from hashlib import sha1

class HopNDrop(ServerPuzzle):

    id = 'hopndrop'

    variants = ["map1"]#, "map2", "map3"]
    
    startRandomized = False

    def __init__(self, variantid="map1", **kwargs):
        self.board = 0
        self.variantid = variantid
        # if key=="map1":
        #     #Map1
        #     self.board = [['-', '-', '1', '1', '1','1'],['-', '1', '1', '-', 'G','1'],['-', '1', '-', '-', '-','-'],['-', '1', '1', '1', '-','-'],['-', 'X(1)', '1', '1', '-','-'],['-', '-', '-', '-', '-','-']]
        #     self.start = [['-', '-', '1', '1', '1','1'],['-', '1', '1', '-', 'G','1'],['-', '1', '-', '-', '-','-'],['-', '1', '1', '1', '-','-'],['-', 'X(1)', '1', '1', '-','-'],['-', '-', '-', '-', '-','-']]
        # elif key=="map2":
        #     #Map2
        #     self.board = [['-','-','-','1','G','-'],['-','-','1','1','-','-'],['-','-','2','1','-','-'],['1','2','2','1','-','-'],['-','X(1)','1','2','1','-'],['-','-','-','-','-','-']]
        #     self.start = [['-','-','-','1','G','-'],['-','-','1','1','-','-'],['-','-','2','1','-','-'],['1','2','2','1','-','-'],['-','X(1)','1','2','1','-'],['-','-','-','-','-','-']]
        # elif key=="map3":
        #     #  Map3
        #     self.board = [['-','-','1','2','G','-'],['-','-','-','1','-','-'],['-','1','2','3','2','1'],['-','1','1','1','1','-'],['-','X(1)','1','-','-','-'],['-','1','1','-','-','-']]
        #     self.start = [['-','-','1','2','G','-'],['-','-','-','1','-','-'],['-','1','2','3','2','1'],['-','1','1','2','1','-'],['-','X(1)','1','-','-','-'],['-','1','1','-','-','-']]
        # elif key=="map4":
        #     self.board = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]
        #     self.start = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]
        # else:
        #     self.board = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]
        #     self.start = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]

    def __str__(self, **kwargs):
        return str(self.board)

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself.
        Example: '5x5', '3x4', 'reverse3x3'
        """
        return self.variantid
        # if self.serialize2(self.start) == '--1111|-11-G1|-1----|-111--|-X(1)11--|------|':
        #     return "map1"
        # elif self.serialize2(self.start) == '---1G-|--11--|--21--|1221--|-X(1)121-|------|':
        #     return "map2"
        # elif self.serialize2(self.start) == '--12G-|---1--|-12321|-1121-|-X(1)1---|-11---|':
        #     return "map3" 
        # elif self.serialize2(self.start) == '---111|11-2G1|X(1)21332|25132-|-211--|------|':
        #     return "map4"

    ### _________ Print Funcs _______________
    def printInfo(self):
        print("Puzzle: ")
        space = "  "
        print(" _______________________________")
        for row in self.board:
            print("| ",end="")
            for i in row:
                if len(i) > 1:
                    print(str(i),end="")
                    print(" ", end="")
                else:
                    print(str(i) + "    ", end="")
            print("|")
        print(" _______________________________")

    # ________ End Print Funcs _________

    def playPuzzle(self, moves):
        print("Enter Piece: ")
        d = {'w':"Up", 'a':"Left", 's':"Down", 'd':"Right"}
        print('| w -> Up | a -> Left | s -> Down | d -> Right |')
        inp = str(input())
        if inp == '':
            return "BEST"
        elif inp not in d.keys():
            return "OOPS"
        else:
            return d[inp]

    def primitive(self, **kwargs):
        return PuzzleValue.SOLVABLE
        # end = False
        # other = True
        # for row in self.board:
        #     for i in row:
        #         if i == 'X(G)':
        #             end = True
        #         elif i != '-':
        #             other = False
        # if end and other:
        #     return PuzzleValue.SOLVABLE
        # else:
        #     return PuzzleValue.UNDECIDED

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        # moves = ["Left","Right", "Up", "Down"]
        return []
        # key = False
        # moves = []
        # if movetype == "all":
        #     key = True
        # if movetype == 'bi':
        #     return []
        # if movetype == 'back' or movetype =='undo' or key:
        #     temp = self.findBackward()
        #     for i in temp:
        #         moves.append(i)
        # if movetype == 'for' or movetype == 'legal' or key:
        #     temp = self.findForward()
        #     for i in temp:
        #         moves.append(i)
        # return moves #default "all"

    ### _____ generateMoves HELPERS _______ ###

    def findBackward(self):
        #Find X
        row_count = 0
        for row in self.board:
            for i in row:
                if 'X' in i:
                    ind = row.index(i)
                    save_row = row_count
                    break
            row_count += 1
        #Check if at start
        if self.board[save_row][ind] == self.start[save_row][ind]:
            return []
        #Check positions around X
        moves = []
        if save_row > 0:
            above = save_row - 1
            if self.start[above][ind] != '-' and self.start[above][ind] != 'G':
                if self.board[above][ind] == '-':
                    moves.append("Up_")
                elif int(self.start[above][ind]) > int(self.board[above][ind]):
                    moves.append("Up_")
        if save_row < len(self.board)-1:
            below = save_row + 1 
            if self.start[below][ind] != '-' and self.start[below][ind] != 'G':
                if self.board[below][ind] == '-':
                    moves.append("Down_")
                elif int(self.start[below][ind]) > int(self.board[below][ind]):
                    moves.append("Down_")
        if ind > 0: 
            left = ind - 1
            if self.start[save_row][left] != '-' and self.start[save_row][left] != 'G':
                if self.board[save_row][left] == '-':
                    moves.append("Left_")
                elif int(self.start[save_row][left]) > int(self.board[save_row][left]):
                    moves.append("Left_")
        if ind < len(self.board[0])-1: #ABOVE
            right = ind + 1
            if self.start[save_row][right] != '-' and self.start[save_row][right] != 'G':
                if self.board[save_row][right] == '-':
                    moves.append("Right_")
                elif int(self.start[save_row][right]) > int(self.board[save_row][right]):
                    moves.append("Right_")
        return moves

    def findForward(self):
        #Find X
        row_count = 0
        ind = 0
        for row in self.board:
            for i in row:
                if 'X' in i and (i[2] == '-' or i[2] =='G'): 
                    return []
                elif 'X' in i:
                    ind = row.index(i)
                    save_row = row_count
                    break
            row_count += 1
        moves = []
        if save_row > 0:
            moves.append("Up")
        if save_row < len(self.board)-1:
            moves.append("Down")
        if ind > 0:
            moves.append("Left")
        if ind < len(self.board[0])-1:
            moves.append("Right")
        return moves

    ### _________ end HELPERS _________________ ###

    def doMove(self, move, **kwargs):
        #Find X
        return [HopNDrop(self.variant)]
        if move not in self.generateMoves(): raise ValueError
        new_board = deepcopy(self.board)
        row_count = 0
        for row in new_board:
            for i in row:
                if 'X' in i:
                    ind = row.index(i)
                    save_row = row_count
                    break
            row_count += 1
        #Check if for/back
        back = False
        if move[-1] == "_":
            back = True
        #Old
        element = new_board[save_row][ind][2]
        if element == 'G':
            t = 0 #nothing
        elif element == '1' and not back:
            element = '-'
        elif not back:
            element = int(element)
            element -= 1
        # else: 
        #     element = int(element)
            # element += 1
        new_board[save_row][ind] = str(element)
        #New
        if move == "Left" or move == "Left_":
            ind -= 1
        if move == "Right" or move == "Right_":
            ind += 1
        if move == "Down" or move == "Down_":
            save_row += 1
        if move == "Up" or move == "Up_":
            save_row -= 1

        if not back:
            element = new_board[save_row][ind]
        elif back:
            element = new_board[save_row][ind]
            if element == '-':
                element = '1'
            else:
                element = int(element)
                element += 1
        new_board[save_row][ind] = 'X(' + str(element) + ')'
        newPuzzle = HopNDrop(key=self.variant)
        newPuzzle.board = new_board
        return newPuzzle

    ### ____________ Solver Funcs ________________

    def __hash__(self):
        # h = sha1()
        # # s = self.serialize()
        # h.update(str(self.board).encode())
        # return int(h.hexdigest(), 16)
        return 0

    def generateSolutions(self, **kwargs):
        #Find G
        return [HopNDrop(self.variant)]
        # newPuzzle = HopNDrop(key=self.variant)
        # row_count = 0
        # for row in newPuzzle.start:
        #     for i in row:
        #         if 'G' in i:
        #             ind = row.index(i)
        #             save_row = row_count
        #             break
        #     row_count += 1
        # board = [['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-']]
        # board[save_row][ind] = 'X(G)'
        # newPuzzle.board = board
        # return [newPuzzle]

    ### ________ Server _________
    @classmethod
    def fromString(cls, variant_id, positionid):
        """Returns a Puzzle object based on positionid
        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))
        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it
        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        return HopNDrop("map1")
        b = [['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-']]
        count = 0
        row = 0
        ind = 0
        for i in positionid:
            if i == "|":
                row +=1
                ind = 0
                continue
            elif i == 'X':
                count = 3
                b[row][ind] = i
                continue
            elif count > 0:
                b[row][ind] += i
                count -= 1
                if count == 0:
                    ind +=1
            else:
                b[row][ind] = i
                ind += 1
        newPuzzle = HopNDrop(key=cls.variant)
        newPuzzle.board = b
        return newPuzzle

    def toString(self, mode):
        """Returns a serialized based on self
        Outputs:
            String Puzzle
        """
        return "Unavailable"
        # out = ""
        # for row in self.board:
        #     for i in row:
        #         out += i
        #     out += "|"
        # return out

    ### Helper for variant function###
    def serialize2(self, s):
        """Returns a serialized based on self
        Outputs:
            String Puzzle
        """
        out = ""
        for row in s:
            for i in row:
                out += i
            out += "|"
        return out

    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        """Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified
        For example, Hanoi cannot have a larger ring on top of a smaller one.
        Outputs:
            - True if Puzzle is valid, else False
        """
        try: puzzle = cls.fromString(positionid)
        except: raise PuzzleException("Position is invalid")
        return True

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in HopNDrop.variants: raise IndexError("Out of bounds variantid")
        return HopNDrop(variantid)
