from ..util import *
from ..puzzles import ServerPuzzle
from hashlib import sha1
import random
import os
dirname = os.path.dirname(__file__)


class Rush(ServerPuzzle):
    id = "rush"
    auth = "Christopher Nammour"
    name = "Rush"
    desc = """Move pieces around to get the red piece to the right side of the board."""
    date = "April 25, 2023"

    variants = ['basic', 'easy', 'medium', 'hard', 'expert']
    startRandomized = False

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str) or variantid not in Rush.variants:
            raise TypeError("Invalid variantid")
        return Rush(variant_id=variantid)

    def __init__(self, variant_id='medium', puzzle_id=None, pos=None):
        super().__init__()
        self.variant_id = variant_id
        if pos is None:
            variant_file = f"{dirname}/../../databases/rush_data/no_walls_{variant_id}.txt"
            if puzzle_id is None:
                # Search the database for a random puzzle with the given difficulty level.
                # variant_ranges = {"basic": 261327, "easy": 59025, "medium": 16351, "hard": 3821, "expert": 1257}
                # puzzle_id = random.randrange(variant_ranges[variant_id])
                puzzle_id = 0
            with open(variant_file, 'r') as variants:
                for i, variant in enumerate(variants):
                    if i == puzzle_id:
                        self.pos = variant[:36]  # remove trailing newline
                        break
        else:
            self.pos = pos

    def __hash__(self):
        h = sha1()
        h.update(self.pos.encode())
        return int(h.hexdigest(), 16)

    @property
    def variant(self):
        return self.variant_id

    def toString(self, mode="minimal"):
        if mode == "minimal":
            return "R_A_" + self.variant_id + "_" + self.pos
        elif mode == "complex":
            display = ""
            for i in range(6):
                display += self.pos[6 * i:6 * (i + 1)] + "\n"
            return display.replace('L', '<')\
                        .replace('R', '>')\
                        .replace('T', 'A')\
                        .replace('B', 'V')\
                        .replace('M', 'H')\
                        .replace('m', '=')\
                        .replace('1', 'X')\
                        .replace('2', 'X')
        else:
            raise ValueError("Invalid keyword argument 'mode'")

    @classmethod
    def fromString(cls, positionid, **kwargs):
        # Checking if the positionid is a str
        if not positionid or not isinstance(positionid, str):
            raise TypeError("PositionID is not type str")
        # Checking if this is a valid string (extract the board first)
        _, _, variant_id, board_string = positionid.split("_")
        if len(board_string) != 36:
            raise ValueError("PositionID cannot be translated into Puzzle")
        # Check that this will decode into a valid board
        try:
            allowed_pieces = {'-', 'L', 'm', 'R', 'T', 'M', 'B', '1', '2'}
            allowed_top = {'-', 'L', 'm', 'R', 'T', '1', '2'}
            allowed_bottom = {'-', 'L', 'm', 'R', 'B'}
            allowed_right = {'-', 'R', 'T', 'M', 'B', '2'}
            allowed_left = {'-', 'L', 'T', 'M', 'B', '1'}
            seen_red_piece = False
            for i, piece in enumerate(board_string):
                # Look through the board, make sure all pieces are allowable pieces
                # and are surrounded by the correct types of pieces
                if piece not in allowed_pieces:
                    raise ValueError
                # Check that edge pieces are allowed to be there
                if i % 6 == 0 and piece not in allowed_left \
                        or i % 6 == 5 and piece not in allowed_right \
                        or i < 6 and piece not in allowed_top \
                        or i >= 30 and piece not in allowed_bottom:
                    raise ValueError
                # Check that there is only one red piece "12" and it is in row 3
                if piece == '1':
                    if seen_red_piece or i < 12 or i > 16:
                        raise ValueError
                    else:
                        seen_red_piece = True
                # Check that the piece to the right is allowed to be on the right of it
                if i % 6 < 5 and (
                        piece == 'L' and board_string[i + 1] not in {'m', 'R'}
                        or piece == 'm' and board_string[i + 1] != 'R'
                        or piece == '1' and board_string[i + 1] != '2'
                        or piece not in {'m', 'L', '1'} and board_string[i + 1] not in allowed_left
                ):
                    raise ValueError
                # Check that the piece below is allowed to be below it
                if i < 30 and (
                        piece == 'T' and board_string[i + 6] not in {'M', 'B'}
                        or piece == 'M' and board_string[i + 6] != 'B'
                        or piece not in {'T', 'M'} and board_string[i + 6] not in allowed_top
                ):
                    raise ValueError
        except ValueError:
            raise ValueError("PositionID cannot be translated into Puzzle")

        # If no error, we can return a board with the given puzzle
        return Rush(variant_id=variant_id, pos=board_string)

    def primitive(self, **kwargs):
        if self.pos[16:18] == "12":
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype="all"):
        if movetype == 'for' or movetype == 'back':
            return []  # All moves are bidirectional
        moves = []
        for i, piece in enumerate(self.pos):
            # Check for leftward moves
            if piece in {'1', 'L'}:
                j = 0
                while (i - j) % 6 > 0 and self.pos[i - j - 1] == '-':
                    j += 1
                    moves.append(f"M_{i}_{i-j}")
            # Check for rightward moves
            elif piece in {'R', '2'}:
                j = 0
                while (i + j) % 6 < 5 and self.pos[i + j + 1] == '-':
                    j += 1
                    moves.append(f"M_{i}_{i+j}")
            # Check for upward moves
            elif piece == 'T':
                j = 1
                while i - 6 * j >= 0 and self.pos[i - 6*j] == '-':
                    moves.append(f"M_{i}_{i-6*j}")
                    j += 1
            # Check for downward moves
            elif piece == 'B':
                j = 1
                while i + 6 * j < 36 and self.pos[i + 6*j] == '-':
                    moves.append(f"M_{i}_{i+6*j}")
                    j += 1
        return moves

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves():
            raise ValueError
        _, start, end = move.split("_")
        start = int(start)
        end = int(end)
        new_pos = list(self.pos)
        # First check the move's orientation to know which way to move
        if end >= start + 6:
            # Downward move, meaning `start` is a 'B' square. Find the entire piece's length to determine what to move.
            length = 2 + (start >= 12 and self.pos[start - 12] == 'T')
            # Move the vertical slice containing the piece, down to the end of the move
            new_pos[(end - 6*(length-1)):(end + 1):6] = self.pos[(start - 6*(length-1)):(start + 1):6]
            # Replace vacated squares by empty '-'
            distance = (end - start) // 6
            new_pos[(start - 6*(length-1)):(end - 6*(length-1)):6] = ['-'] * distance
        elif end > start:
            # Rightward move, meaning `start` is a 'R' square.
            length = 2 + (start % 6 >= 2 and self.pos[start - 2] == 'L')
            new_pos[(end - length + 1):(end + 1)] = self.pos[(start - length + 1):(start + 1)]
            distance = end - start
            new_pos[(start - length + 1):(end - length + 1)] = ['-'] * distance
        elif end <= start - 6:
            # Upward move, meaning `start` is a 'T' square.
            length = 2 + (start < 24 and self.pos[start + 12] == 'B')
            new_pos[end:(end + 6*length):6] = self.pos[start:(start + 6*length):6]
            distance = (start - end) // 6
            new_pos[(end + 6*length):(start + 6*length):6] = ['-'] * distance
        else:
            # Leftward move, meaning `start` is a 'L' square.
            length = 2 + (start % 6 < 4 and self.pos[start + 2] == 'R')
            new_pos[end:(end + length)] = self.pos[start:(start + length)]
            distance = start - end
            new_pos[(end + length):(start + length)] = ['-'] * distance

        return Rush(variant_id=self.variant_id, pos=''.join(new_pos))


# from puzzlesolver.solvers import GeneralSolver
# from puzzlesolver.players import TUI
# puzzle = Rush(variant_id='expert')
# TUI(puzzle, solver=GeneralSolver(puzzle), info=True).play()
# from scripts.server import test_puzzle
# test_puzzle(Rush)

