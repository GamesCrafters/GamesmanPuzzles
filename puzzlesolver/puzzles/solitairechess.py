from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.solvers import SolitaireChessSolver
from puzzlesolver.players import TUI
from puzzlesolver.puzzles import ServerPuzzle

# 0 means no piece, 1 means king piece, 2 means Queen piece, 3 means Rooks, 4 means bishops, 5 means knights, 6 means pawns
PIECE_SYMBOLS = {0: "-", 1: "K", 2: "Q", 3: "R", 4: "B", 5: "N", 6: "P"}
BACKWARDS_PIECE_SYMBOLS = {"-": 0, "K": 1, "Q": 2, "R": 3, "B": 4, "N": 5, "P": 6} 

class SolitaireChess(ServerPuzzle):
    id = 'solitairechess'
    variants = ['1', '2', '3','4','5','6','7','8','9','10']
    startRandomized = False
    
    def __init__(self, variantid='1', **kwargs):
        # TODO: Create functions that generate random stacks for easy / medium / hard
        if variantid == '1':
            self.stacks = [[0, 0, 5, 0], 
                           [0, 1, 0, 0], 
                           [6, 0, 0, 0], 
                           [0, 0, 5, 0]]
        
        if variantid == '2':
            self.stacks = [[0, 0, 0, 0], 
                           [5, 0, 1, 0], 
                           [0, 0, 6, 0], 
                           [2, 2, 0, 0]]
        
        if variantid == '3':
            self.stacks = [[0, 0, 6, 0], 
                           [0, 6, 0, 6], 
                           [6, 0, 6, 0], 
                           [0, 6, 0, 6]]
        if variantid == '4':
            self.stacks = [[0, 5, 0, 0], 
                           [0, 3, 0, 6], 
                           [6, 0, 0, 0], 
                           [3, 0, 0, 2]]
        if variantid=='5':
            self.stacks = [[0, 0, 0, 0], 
                           [2, 0, 0, 0], 
                           [0, 6, 0, 1], 
                           [6, 0, 0, 0]]
        if variantid=='6':
            self.stacks = [[0, 0, 2, 0], 
                           [0, 0, 0, 0], 
                           [5, 0, 0, 0], 
                           [3, 6, 0, 0]]
        if variantid=='7':
            self.stacks = [[2, 0, 0, 0], 
                           [0, 0, 5, 0], 
                           [0, 6, 0, 0], 
                           [3, 0, 0, 6]]
        if variantid=='8':
            self.stacks = [[3, 0, 0, 6], 
                           [0, 6, 0, 0], 
                           [0, 0, 0, 0], 
                           [0, 4, 0, 2]]
        if variantid=='9':
            self.stacks = [[0, 2, 0, 0], 
                           [0, 0, 1, 0], 
                           [0, 0, 0, 2], 
                           [3, 0, 0, 0]]
        if variantid=='10':
            self.stacks = [[0, 0, 5, 0], 
                           [2, 0, 0, 0], 
                           [0, 6, 0, 0], 
                           [0, 0, 3, 0]]



        self.variantid = variantid

    def __hash__(self): # modify this first
        curr_hash = 0
        for i in range(len(self.stacks)):
            for j in range(len(self.stacks)):
                pwr = i * len(self.stacks[i]) + j # row * 4 + col
                curr_hash += self.stacks[i][j] * (10 ** pwr)
        return curr_hash
    
    @property
    def variant(self):
        return self.variantid
    
    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        return SolitaireChess(variantid)
    
    def generateSolutions(self, **kwargs):
        return []

    def toString(self, mode, **kwargs):
        if mode == StringMode.AUTOGUI:
            # GUI toString method
            return_str = '1_'
            for row in self.stacks:
                for position in row:
                    return_str += PIECE_SYMBOLS[position]
            return return_str

        else:
            board_str = ''.join("".join(PIECE_SYMBOLS[piece] for piece in row) for row in self.stacks)
            return f"{board_str}" 
    
    @classmethod
    def fromString(cls, variantid, positionStr):
        stacks = [[],
                  [],
                  [],
                  []]
        for i in range(len(positionStr)): # i goes from 0-15
            # "Human-Readable Position": "--N--K--P-----N-"
            row = i // 4 # determines which row we're adding to
            col = i % 4 # determines which col we're currently adding to; not used in curr implementation
            piece = positionStr[i]
            stacks[row].append(BACKWARDS_PIECE_SYMBOLS[piece])
        
        newPuzzle = SolitaireChess()
        newPuzzle.stacks = stacks
        newPuzzle.variantid = variantid
        return newPuzzle
        
    def moveString(self, move, **kwargs):
        # move is ((start1, start2), (end1, end2)) 
        start_pos = self._convert_move_to_autogui(move[0])
        end_pos = self._convert_move_to_autogui(move[1])
        return f'M_{start_pos}_{end_pos}_x'
    
    def _convert_move_to_autogui(self, move_tuple):
        i, j = move_tuple
        return i * len(self.stacks[0]) + j
    
    def primitive(self, **kwargs):
        total_pieces = sum(piece != 0 for row in self.stacks for piece in row)
        if total_pieces == 1:  # If only one piece is left, it's solved
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def generateMoves(self, movetype="all"):
        moves = []
        for i in range(len(self.stacks)):
            for j in range(len(self.stacks[i])):
                piece = self.stacks[i][j]

                if piece == 0:  # Skip empty spaces
                    continue  
                if piece == 1:  
                    possible_moves = self._get_king_moves(i, j) # contains tuple (moves, undo_moves)
                elif piece == 2:  
                    possible_moves = self._get_queen_moves(i, j)
                elif piece == 3:  
                    possible_moves = self._get_rook_moves(i, j)
                elif piece == 4:  
                    possible_moves = self._get_bishop_moves(i, j)
                elif piece == 5:  
                    possible_moves = self._get_knight_moves(i, j)
                elif piece == 6:  
                    possible_moves = self._get_pawn_moves(i, j)

                # Ensure correct move formatting
                for move in possible_moves:
                    if isinstance(move, tuple) and len(move) == 2:
                        target_x, target_y = move 
                        moves.append(((i, j), (target_x, target_y)))
        return moves

    def doMove(self, move, **kwargs):
        if not isinstance(move, tuple) or len(move) != 2:
            raise TypeError("Move must be a tuple of (start, end) coordinates.")
        
  
        start, end = move
        # Now check if start and end are both tuples with length 2
        if not all(isinstance(x, tuple) and len(x) == 2 for x in [start, end]):
            raise TypeError("Move coordinates must be tuples of (row, col).")
        
        if move not in self.generateMoves('legal'):
            raise ValueError(f"Invalid move attempted.")

        newPuzzle = SolitaireChess()
        newPuzzle.stacks = deepcopy(self.stacks)

        piece = newPuzzle.stacks[start[0]][start[1]]
        newPuzzle.stacks[end[0]][end[1]] = piece  
        newPuzzle.stacks[start[0]][start[1]] = 0 

        return newPuzzle
        

    def _get_king_moves(self, row, col):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 4 and 0 <= nc < 4 and self.stacks[nr][nc] != 0:
                moves.append((nr, nc))
        return moves
    
    def _get_queen_moves(self, row, col):
        return self._get_rook_moves(row, col) + self._get_bishop_moves(row, col)

    def _get_rook_moves(self, row, col):
        moves = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            while 0 <= nr < 4 and 0 <= nc < 4:
                if self.stacks[nr][nc] != 0:
                    moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        
        return moves
    
    def _get_bishop_moves(self, row, col):
        moves = []
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            while 0 <= nr < 4 and 0 <= nc < 4:
                if self.stacks[nr][nc] != 0:
                    moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return moves
    
    def _get_knight_moves(self, row, col):
        moves = []
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 4 and 0 <= nc < 4 and self.stacks[nr][nc] != 0:
                moves.append((nr, nc))
        return moves
    
    def _get_pawn_moves(self, row, col):
        moves = []
        nr = row - 1
        if 0 <= nr < 4:
            for dc in [-1, 1]:
                nc = col + dc
                if 0 <= nc < 4 and self.stacks[nr][nc] != 0:
                    moves.append((nr, nc))
        return moves

# puzzle = SolitaireChess()
# TUI(puzzle, solver=SolitaireChessSolver(puzzle), info=True).play()
