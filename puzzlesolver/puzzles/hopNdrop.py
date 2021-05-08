from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import GeneralSolver, SqliteSolver

from hashlib import sha1

class HopNDrop(ServerPuzzle):

    id      = 'hopNdrop'
    auth    = "Mark Presten"
    name    = "Hop N' Drop"
    desc    = """Clear all platforms before reaching the goal tile. Don't get stuck or fall!"""
    date    = "Oct 10, 2020"

    variants = {
        "map1" : GeneralSolver, 
        "map2" : GeneralSolver, 
        "map3" : GeneralSolver, 
        # "map4" : SqliteSolver
    }

    test_variants = variants

    def __init__(self, key="map1", **kwargs):
        self.var = key
        if self.var == 'map1':
            #Map1
            self.board = [['-', '-', '1', '1', '1','1'],['-', '1', '1', '-', 'G','1'],['-', '1', '-', '-', '-','-'],['-', '1', '1', '1', '-','-'],['-', 'X(1)', '1', '1', '-','-'],['-', '-', '-', '-', '-','-']]
            self.start = [['-', '-', '1', '1', '1','1'],['-', '1', '1', '-', 'G','1'],['-', '1', '-', '-', '-','-'],['-', '1', '1', '1', '-','-'],['-', 'X(1)', '1', '1', '-','-'],['-', '-', '-', '-', '-','-']]
        elif self.var == 'map2':
            #Map2
            self.board = [['-','-','-','1','G','-'],['-','-','1','1','-','-'],['-','-','2','1','-','-'],['1','2','2','1','-','-'],['-','X(1)','1','2','1','-'],['-','-','-','-','-','-']]
            self.start = [['-','-','-','1','G','-'],['-','-','1','1','-','-'],['-','-','2','1','-','-'],['1','2','2','1','-','-'],['-','X(1)','1','2','1','-'],['-','-','-','-','-','-']]
        elif self.var == 'map3':
            #  Map3
            self.board = [['-','-','1','2','G','-'],['-','-','-','1','-','-'],['-','1','2','3','2','1'],['-','1','1','1','1','-'],['-','X(1)','1','-','-','-'],['-','1','1','-','-','-']]
            self.start = [['-','-','1','2','G','-'],['-','-','-','1','-','-'],['-','1','2','3','2','1'],['-','1','1','2','1','-'],['-','X(1)','1','-','-','-'],['-','1','1','-','-','-']]
        elif self.var == 'map4':
            self.board = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]
            self.start = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]

    def __str__(self, **kwargs):
        return str(self.board)

    @property
    def variant(self):
        """Returns a string defining the variant of this puzzleself.
        Example: '5x5', '3x4', 'reverse3x3'
        """
        return self.var

    def update_start(self, var):
        self.var = "map" + var
        if self.var == 'map1':
            #Map1
            self.start = [['-', '-', '1', '1', '1','1'],['-', '1', '1', '-', 'G','1'],['-', '1', '-', '-', '-','-'],['-', '1', '1', '1', '-','-'],['-', 'X(1)', '1', '1', '-','-'],['-', '-', '-', '-', '-','-']]
        elif self.var == 'map2':
            #Map2
            self.start = [['-','-','-','1','G','-'],['-','-','1','1','-','-'],['-','-','2','1','-','-'],['1','2','2','1','-','-'],['-','X(1)','1','2','1','-'],['-','-','-','-','-','-']]
        elif self.var == 'map3':
            # Map3
            self.start = [['-','-','1','2','G','-'],['-','-','-','1','-','-'],['-','1','2','3','2','1'],['-','1','1','2','1','-'],['-','X(1)','1','-','-','-'],['-','1','1','-','-','-']]
        elif self.var == 'map4':
            # Map4
            self.start = [['-', '-', '-', '1', '1', '1'], ['1', '1', '-', '2', 'G', '1'], ['X(1)', '2', '1', '3', '3', '2'], ['2', '5', '1', '3', '2', '-'], ['-', '2', '1', '1', '-', '-'], ['-', '-', '-', '-', '-', '-']]

    def getName(self, **kwargs):
        return "HopNDrop_" + self.var

    def primitive(self, **kwargs):
        end = False
        other = True
        for row in self.board:
            for i in row:
                if i == 'X(G)':
                    end = True
                elif i != '-':
                    other = False
        if end and other:
            return PuzzleValue.SOLVABLE
        else:
            return PuzzleValue.UNDECIDED

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        # moves = ["Left","Right", "Up", "Down"]
        key = False
        moves = []
        if movetype == "all":
            key = True
        if movetype == 'bi':
            return []
        if movetype == 'back' or movetype =='undo' or key:
            temp = self.findBackward()
            for i in temp:
                moves.append(i)
        if movetype == 'for' or movetype == 'legal' or key:
            temp = self.findForward()
            for i in temp:
                moves.append(i)
        return moves #default "all"

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
        from_ = (len(self.board) * save_row) + ind
        if save_row > 0:
            above = save_row - 1
            if self.start[above][ind] != '-' and self.start[above][ind] != 'G':
                if self.board[above][ind] == '-':
                    to_ = (len(self.board) * (save_row - 1)) + ind + (save_row - 1)
                    moves.append("C_{}_{}".format(from_, to_))
                    # moves.append("Up_")
                elif int(self.start[above][ind]) > int(self.board[above][ind]):
                    to_ = (len(self.board)  * (save_row - 1)) + ind + (save_row - 1)
                    moves.append("C_{}_{}".format(from_, to_))                 
                    # moves.append("Up_")
        if save_row < len(self.board)-1:
            below = save_row + 1 
            if self.start[below][ind] != '-' and self.start[below][ind] != 'G':
                if self.board[below][ind] == '-':
                    to_ = (len(self.board) * (save_row + 1)) + ind + (save_row + 1)
                    moves.append("C_{}_{}".format(from_, to_))
                    # moves.append("Down_")
                elif int(self.start[below][ind]) > int(self.board[below][ind]):
                    to_ = (len(self.board) * (save_row + 1)) + ind + (save_row + 1)
                    moves.append("C_{}_{}".format(from_, to_))
                    # moves.append("Down_")
        if ind > 0: 
            left = ind - 1
            if self.start[save_row][left] != '-' and self.start[save_row][left] != 'G':
                if self.board[save_row][left] == '-':
                    to_ = (len(self.board) * save_row) + ind - 1 + save_row
                    moves.append("C_{}_{}".format(from_, to_))
                    # moves.append("Left_")
                elif int(self.start[save_row][left]) > int(self.board[save_row][left]):
                    to_ = (len(self.board) * save_row) + ind - 1 + save_row
                    moves.append("C_{}_{}".format(from_, to_))                    
                    # moves.append("Left_")
        if ind < len(self.board[0])-1: #ABOVE
            right = ind + 1
            if self.start[save_row][right] != '-' and self.start[save_row][right] != 'G':
                if self.board[save_row][right] == '-':
                    to_ = (len(self.board) * save_row) + ind + 1 + save_row
                    moves.append("C_{}_{}".format(from_, to_))
                    # moves.append("Right_")
                elif int(self.start[save_row][right]) > int(self.board[save_row][right]):
                    to_ = (len(self.board) * save_row) + ind + 1 + save_row
                    moves.append("C_{}_{}".format(from_, to_))                    
                    # moves.append("Right_")
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
        from_ = (len(self.board) * save_row) + ind + save_row
        if save_row > 0:
            # moves.append("Up")
            to_ = (len(self.board) * (save_row - 1)) + ind + (save_row - 1)
            moves.append("M_{}_{}".format(from_, to_))
        if save_row < len(self.board)-1:
            # moves.append("Down")
            to_ = (len(self.board) * (save_row + 1)) + ind + (save_row + 1)
            moves.append("M_{}_{}".format(from_, to_))
        if ind > 0:
            # moves.append("Left")
            to_ = (len(self.board) * save_row) + ind - 1 + save_row
            moves.append("M_{}_{}".format(from_, to_))
        if ind < len(self.board[0])-1:
            # moves.append("Right")
            to_ = (len(self.board) * save_row ) + ind + 1 + save_row
            moves.append("M_{}_{}".format(from_, to_))
        return moves

    ### _________ end HELPERS _________________ ###

    def doMove(self, move, **kwargs):
        #Find X
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
        if move[0] == "C":
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
        parts = move.split('_')
        from_ = self.convert_ind(int(parts[1]))
        to_ = self.convert_ind(int(parts[2]))
        if from_ - to_ == 1: #Left
            ind -= 1
        if from_ - to_ == -1: #Right
            ind += 1
        if from_ - to_ == -len(self.board): #Down
            save_row += 1
        if from_ - to_ == len(self.board): #Up
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

    def convert_ind(self, num):
        if num <= 5:
            return num
        elif num >= 7 and num <= 12:
            return num - 1
        elif num >= 14 and num <= 19:
            return num - 2
        elif num >= 21 and num <= 26:
            return num - 3
        elif num >= 28 and num <= 33:
            return num - 4
        elif num >= 35 and num <= 40:
            return num - 5
    ### ____________ Solver Funcs ________________

    def __hash__(self):
        h = sha1()
        # s = self.serialize()
        h.update(str(self.board).encode())
        return int(h.hexdigest(), 16)

    def generateSolutions(self, **kwargs):
        #Find G
        newPuzzle = HopNDrop(key=self.variant)
        row_count = 0
        for row in newPuzzle.start:
            for i in row:
                if 'G' in i:
                    ind = row.index(i)
                    save_row = row_count
                    break
            row_count += 1
        board = [['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-'],['-', '-', '-', '-', '-','-']]
        board[save_row][ind] = 'X(G)'
        newPuzzle.board = board
        return [newPuzzle]

    ### ________ Server _________
    @classmethod
    def fromString(cls, positionid, **kwargs):
        """Returns a Puzzle object based on positionid
        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))
        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it
        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        dic = {'a':'1','b':'2', 'c':'3', 'd':'4', 'e':'5', '-':'-', 'x':'G', 'o':'-'}
        b = [['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-'],['-','-','-','-','-','-']]
        positionid = positionid[8:]
        row = 0
        ind = 0
        last_col = 0
        var = None
        for i in positionid:
            last_col += 1
            if last_col % (len(b)+1) == 0:
                if row == 0:
                    var = i 
                    continue
                else:
                    continue
            if ind % len(b) == 0 and ind != 0:
                row += 1
            curr_ind = ind % len(b)
            if i.isupper():
                b[row][curr_ind] = 'X(' + dic[i.lower()] + ')'
            else:
                b[row][curr_ind] = dic[i]
            ind += 1 
        newPuzzle = HopNDrop(key=cls.variant)
        newPuzzle.board = b
        newPuzzle.update_start(var)
        return newPuzzle

    def toString(self, mode="minimal"):
        """Returns a serialized based on self
        Outputs:
            String Puzzle
        """
        dic = {'1':'a', '2':'b', '3':'c', '4':'d', '5':'e', '-':'-', 'G':'x'}
        if mode == "minimal":
            out = ""
            avoid = 0
            first_row = True
            for row in self.board:
                for item in range(len(row)+1):
                    if item == len(row): 
                        if first_row:
                            out += self.var[-1] #modify to be variant
                            first_row = False
                        else:
                            out += '*'
                    else:
                        i = row[item]
                        if i[0] == 'X':
                            under = dic[i[2]]
                            if under == '-':
                                out += 'O'
                            else:
                                out += under.upper()
                        else:
                            out += dic[i]
            output = "R_{}_{}_{}_".format("A", len(self.board)+1, len(self.board)+1) + out
            return output
        elif mode == "complex":
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
        else:
            raise ValueError("Invalid keyword argument 'mode'")

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
        return True

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in HopNDrop.variants: raise IndexError("Out of bounds variantid")
        return HopNDrop(key = variantid)

    ### _________ Print Funcs _______________

    def playPuzzle(self, moves):
        print("Enter Piece: ")
        d = ['w', 'a', 's', 'd']
        print('| w -> Up | a -> Left | s -> Down | d -> Right |')
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
        from_ = (len(self.board) * save_row) + ind
        inp = str(input())
        if inp == '':
            return "BEST"
        elif inp not in d:
            return "OOPS"
        else:
            if inp == 'w':
                to_ = (len(self.board) * (save_row - 1)) + ind                
                return "M_{}_{}".format(from_, to_)
            if inp == 'a':
                to_ = (len(self.board) * save_row) + ind - 1
                return "M_{}_{}".format(from_, to_)
            if inp == 's':
                to_ = (len(self.board) * (save_row + 1)) + ind                
                return "M_{}_{}".format(from_, to_)
            if inp == 'd':
                to_ = (len(self.board) * save_row) + ind + 1
                return "M_{}_{}".format(from_, to_)