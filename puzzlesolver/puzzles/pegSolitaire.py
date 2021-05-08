from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import SqliteSolver, GeneralSolver

from hashlib import sha1

UNMAP_MOVES = {0:[0,0], 5:[1,0], 6:[1,1], 10:[2,0], 11:[2,1], 12:[2,2], 15:[3,0],
    16:[3,1], 17:[3,2], 18:[3,3], 20:[4,0], 21:[4,1], 22:[4,2], 23:[4,3], 24:[4,4]}

UWAPI_MOVES = {str([0,0]):0, str([1,0]):5, str([1,1]):6, str([2,0]):10, str([2,1]):11, str([2,2]):12, str([3,0]):15,
    str([3,1]):16, str([3,2]):17, str([3,3]):18, str([4,0]):20, str([4,1]):21, str([4,2]):22, str([4,3]):23, str([4,4]):24}

class Peg(ServerPuzzle):

    id      = 'pegSolitaire'
    auth    = "Mark Presten"
    name    = "Peg Solitaire"
    desc    = """Jump over a peg with an adjacent peg, removing it from the board. Have one peg remaining by end of the game."""
    date    = "April 15, 2020"

    variants = {"Triangle": SqliteSolver}
    test_variants = variants

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

    @property
    def variant(self):
        return "Triangle"

    ### _________ Print Funcs _______________

    def getName(self, **kwargs):
        return "Peg_Solitaire_" + self.variant

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
        
        new_moves = ["M_{}_{}".format(UWAPI_MOVES[str(i[0])], UWAPI_MOVES[str(i[1])]) for i in moves]
        return new_moves

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
        if move not in self.generateMoves(): raise ValueError

        new_board = deepcopy(self.board)
        parts = move.split("_")
        from_peg = UNMAP_MOVES[int(parts[1])] 
        to_peg = UNMAP_MOVES[int(parts[2])] 
        new_board[from_peg[0]][from_peg[1]] = 0
        new_board[to_peg[0]][to_peg[1]] = 1
        #find middle peg to set to ZERO OR ONE
        #h
        if from_peg[0] == to_peg[0]:
            if from_peg[1] > to_peg[1]:
                new_board[from_peg[0]][from_peg[1] - 1] ^= 1
            else:
                new_board[from_peg[0]][from_peg[1] + 1] ^= 1
        #lv
        elif from_peg[1] == to_peg[1]:
            if from_peg[0] > to_peg[0]:
                new_board[from_peg[0] - 1][from_peg[1]] ^= 1
            else:
                new_board[from_peg[0] + 1][from_peg[1]] ^= 1
        #rv
        else:
            if from_peg[0] > to_peg[0]:
                new_board[from_peg[0] - 1][from_peg[1] - 1] ^= 1
            else: 
                new_board[from_peg[0] + 1][from_peg[1] + 1] ^= 1

        newPuzzle = Peg(board=new_board)
        return newPuzzle

    ### ____________ Solver Funcs ________________

    def __hash__(self):
        h = sha1()
        h.update(str(self.board).encode())
        return int(h.hexdigest(), 16)

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Peg.variants: raise IndexError("Out of bounds variantid")
        return Peg(board=[[0],[1,1],[1,1,1],[1,1,1,1],[1,1,1,1,1]])

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
        positionid = positionid[8:]
        new_board = []
        temp = []
        count = 1
        for item in positionid:
            if item == "*":
                continue
            if item == "1":
                temp.append(1)
            if item == "-":
                temp.append(0)
            count -= 1
            if count == 0:
                new_board.append(temp)
                count = len(temp) + 1
                temp = []
        return Peg(board=new_board)

    def toString(self, mode="minimal"):
        if mode == "minimal":   
            output = "R_{}_{}_{}_".format("A", len(self.board), len(self.board))
            to_join = []
            for row in self.board:
                padding = "*" * (5 - len(row))
                nxt = [str(x) if x == 1 else '-' for x in row]
                nxt.append(padding)
                to_join.append("".join(nxt))
            return output + "".join(to_join)
        elif mode == "complex":
            d = {str([0,0]):'[A]', str([1,0]):'[B]', str([1,1]):'[C]', str([2,0]):'[D]', str([2,1]):'[E]', str([2,2]):'[F]', str([3,0]):'[G]',
                str([3,1]):'[H]', str([3,2]):'[I]', str([3,3]):'[J]', str([4,0]):'[K]', str([4,1]):'[L]', str([4,2]):'[M]', str([4,3]):'[N]', str([4,4]):'[O]'}
            space = 20 * " "
            output = ""
            for outer in range(5):
                output += space
                for inner in range(outer + 1):
                    output += str(self.board[outer][inner]) + "       "
                output += "\n"
                temp = list(space)
                temp = temp[:-4]
                space = "".join(temp)
                output += " " + space + " "
                for inner2 in range(outer + 1):
                    output += " " +d[str([outer, inner2])] + "    "
                output += "\n"
            return output
        else:
            raise ValueError("Invalid keyword argument 'mode'")

    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        """Checks if the Puzzle is valid given the rules.
        For example, Hanoi cannot have a larger ring on top of a smaller one.
        Outputs:
            - True if Puzzle is valid, else False
        """
        try: puzzle = cls.fromString(positionid)
        except: return False
        if puzzle.pins == 15 or puzzle.pins == 0:
            return False
        return True

    def generateSolutions(self, **kwargs):
        solutions = []
        for outer in range(5):
            for inner in range(outer + 1):
                temp_board = [[0],[0,0],[0,0,0],[0,0,0,0],[0,0,0,0,0]]
                temp_board[outer][inner] = 1
                newPuzzle = Peg(board=temp_board)
                solutions.append(newPuzzle)
        return solutions

    # _____________ TUI __________________

    def playPuzzle(self, moves):
        MAP_MOVES_TUI = {0:'[A]', 5:'[B]', 6:'[C]', 10:'[D]', 11:'[E]', 12:'[F]', 15:'[G]',
            16:'[H]', 17:'[I]', 18:'[J]', 20:'[K]', 21:'[L]', 22:'[M]', 23:'[N]', 24:'[O]'}

        print("Possible Moves: ")
        new_moves = {}
        for move in moves:
            parts = move.split('_')
            print(MAP_MOVES_TUI[int(parts[1])] + '->' + MAP_MOVES_TUI[int(parts[2])])
            from_peg = MAP_MOVES_TUI[int(parts[1])][1].lower()
            to_peg = MAP_MOVES_TUI[int(parts[2])][1].lower()
            new_moves[from_peg + to_peg] = move
        print("| Type starting peg to ending peg in lower case, e.g. for [D]->[A], type 'da' |")
        inp = str(input())
        if inp == '':
            return "BEST"
        from_peg = inp[0].upper()
        to_peg = inp[1].upper()
        if len(inp) != 2 or inp not in new_moves:
            return "OOPS"
        return new_moves[inp]

