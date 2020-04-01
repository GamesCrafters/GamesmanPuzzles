from copy import deepcopy
from .puzzle import Puzzle
from ..util import *
from ..solvers import GeneralSolver
from ..puzzleplayer import PuzzlePlayer

class Peg(Puzzle):
    def __init__(self, **kwargs):
        if len(kwargs) == 1:
            for key,value in kwargs.items():
                if key=='board':
                    self.board = value #[[0],[1,1],[1,1,1],[1,1,1,1],[1,1,1,1,1]] 
                    self.pins = 0
                    for outer in range(5):
                        for inner in range(outer + 1):
                            if self.board[outer][inner] == 1:
                                self.pins += 1  
        else:    
            self.board = [[0],[1,1],[1,1,1],[1,1,1,1],[1,1,1,1,1]] 
            self.pins = 0
            for outer in range(5):
                for inner in range(outer + 1):
                    if self.board[outer][inner] == 1:
                        self.pins += 1  

    def __str__(self, **kwargs):
        return str(self.board)

    ### _________ Print Funcs _______________
    def printInfo(self):
        #Print Puzzle
        print("Puzzle: ")
        space = "                    "
        for outer in range(5):
            print(space, end="")
            for inner in range(outer + 1):
                print(str(self.board[outer][inner]) + "       ", end="")
            print("")
            temp = list(space)
            temp = temp[:-4]
            space = "".join(temp)
            print(" " + space + " ", end="")
            for inner2 in range(outer + 1):
                print("[" + str(outer) + "," + str(inner2) + "]" + "   ", end="")
            print("")

    def getName(self, **kwargs):
        return "Peg Solitaire"

    # ________ End Print Funcs _________

    def primitive(self, **kwargs):
        if self.pins == 1:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    # Generate Legal Movees & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = []
        key = False
        if movetype=='bi':
            return []
        if movetype=='all':
            key = True
        if movetype=='for' or movetype=='legal' or key:
            for outer in range(5):
                for inner in range(outer + 1):
                    if self.board[outer][inner] == 1: #for each peg
                        #LV
                        check1 = self.search_lv([outer, inner], True)
                        check1_len = len(check1)
                        for i in range(check1_len):
                            moves.append(check1[i])
                        #RV
                        check2 = self.search_rv([outer, inner], True)
                        check2_len = len(check2)
                        for i in range(check2_len):
                            moves.append(check2[i])
                        #HV
                        check3 = self.search_h([outer, inner], True)
                        check3_len = len(check3)
                        for i in range(check3_len):
                            moves.append(check3[i])        
        if movetype=='undo' or movetype=='back' or key:
            for outer in range(5):
                for inner in range(outer + 1):
                    if self.board[outer][inner] == 1: #for each peg
                        #LV
                        check1 = self.search_lv([outer, inner], False)
                        check1_len = len(check1)
                        for i in range(check1_len):
                            moves.append(check1[i])
                        #RV
                        check2 = self.search_rv([outer, inner], False)
                        check2_len = len(check2)
                        for i in range(check2_len):
                            moves.append(check2[i])
                        #HV
                        check3 = self.search_h([outer, inner], False)
                        check3_len = len(check3)
                        for i in range(check3_len):
                            moves.append(check3[i])
        return moves

    ### _____ generateMoves HELPERS _______ ###
    
    # left vertical
    def search_lv(self, peg, legal):
        moves = []
        out_ind = peg[0]
        inn_ind = peg[1]
        # (up)
        check_out = out_ind - 1
        if check_out >= 0 and inn_ind <= check_out:
            if self.board[check_out][inn_ind] == 0:
                # start undo
                if not legal:
                    check_out = out_ind - 2
                    if check_out >= 0 and inn_ind <= check_out:
                        if self.board[check_out][inn_ind] == 0:
                            moves.append([[out_ind, inn_ind], [check_out, inn_ind], 'undo'])
                # end undo
                else:                  
                    check_out = out_ind + 1
                    if check_out <= 4:
                        if self.board[check_out][inn_ind] == 1:
                            moves.append([[out_ind + 1, inn_ind],[out_ind - 1, inn_ind]])
        # (down)
        check_out = out_ind + 1
        if check_out <= 4:
            if self.board[check_out][inn_ind] == 0:
                # start undo
                if not legal:
                    check_out = out_ind + 2
                    if check_out <= 4:
                        if self.board[check_out][inn_ind] == 0:
                            moves.append([[out_ind, inn_ind], [check_out, inn_ind], 'undo'])
                # end undo 
                else:   
                    check_out = out_ind - 1
                    if check_out >= 0 and inn_ind <= check_out:
                        if self.board[check_out][inn_ind] == 1:
                            moves.append([[out_ind - 1, inn_ind],[out_ind + 1, inn_ind]])
        return moves

    # right vertical
    def search_rv(self, peg, legal):
        moves = []
        out_ind = peg[0]
        inn_ind = peg[1]
        # (up)
        check_out = out_ind - 1
        check_inn = inn_ind - 1
        if check_out >= 0 and check_inn >= 0:
            if self.board[check_out][check_inn] == 0:
                # start undo
                if not legal:
                    check_out = out_ind - 2
                    check_inn = inn_ind - 2
                    if check_out >= 0 and check_inn >= 0:
                        if self.board[check_out][check_inn] == 0:
                            moves.append([[out_ind, inn_ind], [check_out, check_inn], 'undo'])
                # end undo
                else:               
                    check_out = out_ind + 1
                    check_inn = inn_ind + 1
                    if check_out <= 4:
                        if self.board[check_out][check_inn] == 1:
                            moves.append([[out_ind + 1, inn_ind + 1], [out_ind - 1, inn_ind - 1]])
        # (down)
        check_out = out_ind + 1
        check_inn = inn_ind + 1
        if check_out <= 4:
            if self.board[check_out][check_inn] == 0:
                # start undo
                if not legal:
                    check_out = out_ind + 2
                    check_inn = inn_ind + 2
                    if check_out <= 4:
                        if self.board[check_out][check_inn] == 0:
                            moves.append([[out_ind, inn_ind], [check_out, check_inn], 'undo'])
                # end undo
                else:                 
                    check_out = out_ind - 1
                    check_inn = inn_ind - 1
                    if check_out >= 0 and check_inn >= 0:
                        if self.board[check_out][check_inn] == 1:
                            moves.append([[out_ind - 1, inn_ind - 1], [out_ind + 1, inn_ind + 1]])
        return moves

    #horizontal
    def search_h(self, peg, legal):
        moves = []
        out_ind = peg[0]
        inn_ind = peg[1]
        # (right)
        check_inn = inn_ind + 1
        if check_inn <= out_ind:
            if self.board[out_ind][check_inn] == 0:
                # start undo
                if not legal:
                    check_inn = inn_ind + 2
                    if check_inn <= out_ind:
                        if self.board[out_ind][check_inn] == 0:
                            moves.append([[out_ind, inn_ind], [out_ind, check_inn], 'undo'])
                # end undo
                else:
                    check_inn = inn_ind - 1
                    if check_inn >= 0:
                        if self.board[out_ind][check_inn] == 1:
                            moves.append([[out_ind, inn_ind - 1], [out_ind, inn_ind + 1]])
        # (left)
        check_inn = inn_ind - 1
        if check_inn >= 0:
            if self.board[out_ind][check_inn] == 0:
                # start undo
                if not legal:
                    check_inn = inn_ind - 2
                    if check_inn >= 0:
                        if self.board[out_ind][check_inn] == 0:
                            moves.append([[out_ind, inn_ind], [out_ind, check_inn], 'undo'])
                # end undo
                else:
                    check_inn = inn_ind + 1
                    if check_inn <= out_ind:
                        if self.board[out_ind][check_inn] == 1:
                            moves.append([[out_ind, inn_ind + 1], [out_ind, inn_ind - 1]])
        return moves

    ### _________ end HELPERS _________________ ###

    def doMove(self, move, **kwargs):
        new_board = deepcopy(self.board)
        from_peg = move[0]
        to_peg = move[1]
        new_board[from_peg[0]][from_peg[1]] = 0
        new_board[to_peg[0]][to_peg[1]] = 1
        #find middle peg to set to ZERO OR ONE
        if len(move) == 3:
            set_num = 1
        else:
            set_num = 0
        #h
        if from_peg[0] == to_peg[0]:
            if from_peg[1] > to_peg[1]:
                new_board[from_peg[0]][from_peg[1] - 1] = set_num
            else:
                new_board[from_peg[0]][from_peg[1] + 1] = set_num
        #lv
        elif from_peg[1] == to_peg[1]:
            if from_peg[0] > to_peg[0]:
                new_board[from_peg[0] - 1][from_peg[1]] = set_num
            else: 
                new_board[from_peg[0] + 1][from_peg[1]] = set_num
        #rv
        else:
            if from_peg[0] > to_peg[0]:
                new_board[from_peg[0] - 1][from_peg[1] - 1] = set_num
            else: 
                new_board[from_peg[0] + 1][from_peg[1] + 1] = set_num

        newPuzzle = Peg(board=new_board)
        return newPuzzle

    ### ____________ Solver Funcs ________________

    def __hash__(self):
        return hash(str(self.board))

    def generateSolutions(self, **kwargs):
        solutions = []
        for outer in range(5):
            for inner in range(outer + 1):
                temp_board = [[0],[0,0],[0,0,0],[0,0,0,0],[0,0,0,0,0]]
                temp_board[outer][inner] = 1
                newPuzzle = Peg(board=temp_board)
                solutions.append(newPuzzle)
        return solutions

                

board = [[1],[0,1],[1,1,1],[1,1,1,1],[1,1,1,1,1]]
board2 = [[0],[0,0],[0,0,0],[1,0,0,0],[1,0,0,0,0]]

PuzzlePlayer(Peg(board=board), solver=GeneralSolver(), auto=False).play()
# PuzzlePlayer(Peg()).play()

