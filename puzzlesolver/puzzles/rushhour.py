"""
File: rushhour.py
Puzzle: Rush Hour
Author: Christopher Nammour
Date: April 25, 2023
"""


from ..util import *
from ..puzzles import ServerPuzzle
import random
import os
dirname = os.path.dirname(__file__)


class RushHour(ServerPuzzle):
    id = "rushhour"
    variants = ['basic', 'easy', 'medium', 'hard', 'expert']
    # "True" would mean that the game would start at a random solvable board,
    # by looking at all solvable hashes -- hence False to ensure we fix a start position
    startRandomized = False

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str) or variantid not in RushHour.variants:
            raise TypeError("Invalid variantid")
        return RushHour(variant_id=variantid)

    def __init__(self, variant_id, puzzle_id=None, pos=None):
        super().__init__()
        self.variant_id = variant_id
        if pos is None:
            variant_file = f"{dirname}/../assets/rushhour/{variant_id}.txt"
            if puzzle_id is None:
                # Search the database for a random puzzle with the given difficulty level.
                variant_ranges = {"basic": 4943, "easy": 4998, "medium": 5000, "hard": 4043, "expert": 1336}
                puzzle_id = random.randrange(variant_ranges[variant_id])
            with open(variant_file, 'r') as variants:
                for i, variant in enumerate(variants):
                    if i == puzzle_id:
                        self.pos = variant[:36] + "--"  # remove trailing newline
                        break
        else:
            self.pos = pos

    @property
    def variant(self):
        return self.variant_id

    def __hash__(self):
        # At each step, add to the total, and multiply by the number of options
        result = 0
        multiplier = 1
        # First hash the position of the red piece
        red_pos = list(self.pos[12:17]).index("1")
        result += red_pos
        multiplier *= 5
        # Then the every other remaining piece in the third row
        for i in range(12, 18, 2):
            if i % 6 == red_pos or i % 6 == red_pos + 1:
                continue
            result += ['-', 'T', 'M', 'B'].index(self.pos[i]) * multiplier
            multiplier *= 4
        # Then the top-left piece
        result += ['-', 'L', 'T'].index(self.pos[0]) * multiplier
        multiplier *= 3
        # Finally every other piece on the rest of the grid
        for j in range(2, 36):
            # "every other piece" means row+column is even [also exclude the third row]
            if j // 6 == 2 or ((j % 6) + (j // 6)) % 2 != 0:
                continue
            allowed_pieces = ['-', 'L', 'm', 'R', 'T', 'M', 'B']
            if j % 6 == 0:
                allowed_pieces = ['-', 'L', 'T', 'M', 'B']
            elif j % 6 == 5:
                allowed_pieces = ['-', 'R', 'T', 'M', 'B']
            elif j // 6 == 0:
                allowed_pieces = ['-', 'L', 'm', 'R', 'T']
            elif j // 6 == 5:
                allowed_pieces = ['-', 'L', 'm', 'R', 'B']
            result += allowed_pieces.index(self.pos[j]) * multiplier
            multiplier *= len(allowed_pieces)
        return result

    @classmethod
    def fromHash(cls, variantid, hash_val):
        # Invert the steps in __hash__ to find every other piece in the board
        new_pos = ['-'] * 38
        # First the red piece
        red_pos = hash_val % 5
        new_pos[12 + red_pos] = '1'
        new_pos[12 + red_pos + 1] = '2'
        hash_val //= 5
        # Then every other piece in the third row
        for i in range(12, 18, 2):
            if i % 6 == red_pos or i % 6 == red_pos + 1:
                continue
            new_pos[i] = ['-', 'T', 'M', 'B'][hash_val % 4]
            hash_val //= 4
        # Then the top-left piece
        new_pos[0] = ['-', 'L', 'T'][hash_val % 3]
        hash_val //= 3
        # Finally every other piece on the rest of the grid
        for i in range(2, 36):
            if i // 6 == 2 or ((i % 6) + (i // 6)) % 2 != 0:
                continue
            allowed_pieces = ['-', 'L', 'm', 'R', 'T', 'M', 'B']
            if i % 6 == 0:
                allowed_pieces = ['-', 'L', 'T', 'M', 'B']
            elif i % 6 == 5:
                allowed_pieces = ['-', 'R', 'T', 'M', 'B']
            elif i // 6 == 0:
                allowed_pieces = ['-', 'L', 'm', 'R', 'T']
            elif i // 6 == 5:
                allowed_pieces = ['-', 'L', 'm', 'R', 'B']
            n = len(allowed_pieces)
            new_pos[i] = allowed_pieces[hash_val % n]
            hash_val //= n
        # Once we have every other piece, extrapolate the rest of the board
        for i in range(1, 36):
            if new_pos[i] != '-' or ((i % 6) + (i // 6)) % 2 == 0:
                continue
            if i % 6 > 0 and new_pos[i - 1] in {'L', 'm'}:
                if i % 6 < 5 and new_pos[i + 1] == 'R':
                    new_pos[i] = 'm'
                else:
                    new_pos[i] = 'R'
            elif i % 6 < 5 and new_pos[i + 1] in {'R', 'm'}:
                new_pos[i] = 'L'
            elif i >= 6 and new_pos[i - 6] in {'T', 'M'}:
                if i < 30 and new_pos[i + 6] == 'B':
                    new_pos[i] = 'M'
                else:
                    new_pos[i] = 'B'
            elif i < 30 and new_pos[i + 6] in {'B', 'M'}:
                new_pos[i] = 'T'
        return RushHour(variantid, pos=''.join(new_pos))

    def toString(self, mode):
        if mode == StringMode.HUMAN_READABLE_MULTILINE:
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
            entity_string = self.to_winning_string()
            if mode == StringMode.AUTOGUI:
                return f'1_{entity_string}'
            else:
                return entity_string

    def to_winning_string(self):
        """Converts a winning position to a string representation of it:
        moves the red piece out to the last two indices in the string.
        If not in a winning position, does nothing."""
        if self.pos[16:18] == "12":
            return self.pos[:16] + "--" + self.pos[18:36] + "12"
        else:
            return self.pos

    @staticmethod
    def from_winning_string(board_string):
        """Inverts to_winning_string: moves the red piece from the last
        two indices in the string (if it is there) back inside the board.
        Assumes this is a standard board string of length 38, in a valid winning position."""
        if board_string[-2:] == "12":
            return board_string[:16] + "12" + board_string[18:36] + "--"
        else:
            return board_string

    @classmethod
    def fromString(cls, variant_id, board_string):
        # Checking if the positionid is a str
        if not board_string or not isinstance(board_string, str):
            raise TypeError("PositionID is not type str")
        # Checking if this is a valid string (extract the board and difficulty first)

        if len(board_string) != 38:
            raise ValueError("PositionID cannot be translated into Puzzle")
        # Check that the last two characters are either empty or the red piece in a winning state
        if not (board_string[-2:] == "--" or
                board_string[-2:] == "12" and board_string[16:18] == "--"):
            raise ValueError("PositionID cannot be translated into Puzzle")
        # Move the red piece back into the board if it's outside
        board_string = RushHour.from_winning_string(board_string)
        # Check that this will decode into a valid board
        try:
            allowed_pieces = {'-', 'L', 'm', 'R', 'T', 'M', 'B', '1', '2'}
            allowed_top = {'-', 'L', 'm', 'R', 'T', '1', '2'}
            allowed_bottom = {'-', 'L', 'm', 'R', 'B'}
            allowed_right = {'-', 'R', 'T', 'M', 'B', '2'}
            allowed_left = {'-', 'L', 'T', 'M', 'B', '1'}
            seen_red_piece = False
            for i, piece in enumerate(board_string[:36]):
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
            if not seen_red_piece:
                raise ValueError
        except ValueError:
            raise ValueError("PositionID cannot be translated into Puzzle")

        # If no error, we can return a board with the given puzzle.
        return RushHour(variant_id=variant_id, pos=board_string)

    def primitive(self, **kwargs):
        if self.pos[16:18] == "12":
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype="all"):
        if movetype == 'for' or movetype == 'back':
            return []  # All moves are bidirectional
        moves = []
        for i, piece in enumerate(self.pos[:36]):
            # Check for leftward moves
            if piece in {'1', 'L'}:
                j = 0
                while (i - j) % 6 > 0 and self.pos[i - j - 1] == '-':
                    j += 1
                    if i == 16:
                        # If it's a leftward move from a winning position,
                        # display it as though it is coming from outside the grid
                        moves.append(f"M_{36}_{i-j}_x")
                    else:
                        moves.append(f"M_{i}_{i-j}_x")
            # Check for rightward moves
            elif piece in {'R', '2'}:
                j = 0
                while (i + j) % 6 < 5 and self.pos[i + j + 1] == '-':
                    j += 1
                    if i + j == 17:
                        # If it's a rightward move to a winning position,
                        # display it as though it is going outside the grid
                        moves.append(f"M_{i}_{36}_x")
                    else:
                        moves.append(f"M_{i}_{i+j}_x")
            # Check for upward moves
            elif piece == 'T':
                j = 1
                while i - 6 * j >= 0 and self.pos[i - 6*j] == '-':
                    moves.append(f"M_{i}_{i-6*j}_x")
                    j += 1
            # Check for downward moves
            elif piece == 'B':
                j = 1
                while i + 6 * j < 36 and self.pos[i + 6*j] == '-':
                    moves.append(f"M_{i}_{i+6*j}_x")
                    j += 1
        return moves

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves():
            raise ValueError
        _, start, end, _ = move.split("_")
        start = int(start)
        end = int(end)
        # If the move is to/from a winning position, adjust to the true destination (see generateMoves)
        if start == 36: start = 16
        if end == 36: end = 17
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

        return RushHour(variant_id=self.variant_id, pos=''.join(new_pos))
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            return move
        else:
            parts = move.split('_')
            return f'{parts[1]} {parts[2]}'
