from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI
from hashlib import sha1
import random


class Rush(ServerPuzzle):
    id = "rush"
    auth = "Christopher Nammour"
    name = "Rush"
    desc = """Move pieces around to get the red piece to the right side of the board."""
    date = "April 25, 2023"

    # basic, easy, medium, hard, expert
    variants = map(str, range(5))

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str):
            raise TypeError("Invalid variantid")
        if int(variantid) >= 5:
            raise ValueError("Out of bounds variantid")
        return Rush(variant_id=int(variantid))

    def __init__(self, variant_id=2, puzzle_id=None, pos=None):
        super().__init__()
        self.variant_id = variant_id
        if not pos:
            if not puzzle_id:
                # Search the database for a random puzzle with the given difficulty level.
                variant_ranges = [(80454, 261327), (21429, 80454), (5076, 21429), (1257, 5076), (0, 1257)]
                min_id, max_id = variant_ranges[variant_id]
                puzzle_id = random.randrange(min_id, max_id)
            with open("rush_data/no_walls.txt") as variants:
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

    def toString(self, **kwargs):
        display = ""
        for i in range(6):
            display += self.pos[6 * i:6 * (i + 1)] + "\n"
        return display

    @classmethod
    def fromString(cls, positionid, **kwargs):
        # Checking if the positionid is a str
        if not isinstance(positionid, str):
            raise TypeError("PositionID is not type str")
        # Checking if this is a valid string
        if not positionid or len(positionid) != 36:
            raise ValueError("PositionID cannot be translated into Puzzle")
        # Check that this will decode into a valid board
        try:
            # Keep track of all seen letters, map them to their start indices, lengths, and orientations
            seen = {}
            for i, piece in enumerate(positionid):
                # Look through the board, make sure all pieces are either right or down pieces
                # And make sure no pieces form a non-straight line, or a line of length >3
                if piece == 'o':
                    continue
                # If we've seen it before, and it's not below/to the right of its start, error
                if piece in seen:
                    start, length, orientation = seen[piece]
                    if (orientation == 'R' and i - start >= length
                            or orientation == 'D' and ((i - start) % 6 != 0 or (i - start) / 6 >= length)):
                        raise ValueError
                    else:
                        continue
                # Otherwise, check for orientation, check if length > 2, and add it to the dict
                # Any future pieces outside that orientation / length range will cause an error
                if i % 6 < 5 and positionid[i+1] == piece:
                    length = 2 + (i < 34 and positionid[i + 2] == piece)
                    seen[piece] = (i, length, 'R')
                elif i < 30 and positionid[i+6] == piece:
                    length = 2 + (i < 24 and positionid[i + 12] == piece)
                    seen[piece] = (i, length, 'D')
                else:
                    raise ValueError
        except ValueError:
            raise ValueError("PositionID cannot be translated into Puzzle")

        # If no error, we can return a board with the given puzzle
        return Rush(pos=positionid)

    def primitive(self, **kwargs):
        if self.pos[16:18] == "AA":
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype="all"):
        if movetype == 'for' or movetype == 'back':
            return []  # All moves are bidirectional
        moves = []
        visited = []  # keep track of which pieces we've seen, by letter
        for i, piece in enumerate(self.pos):
            if piece == 'o' or piece in visited:
                continue
            visited.append(piece)
            # Check for moves left and right. First check the piece's orientation.
            # Since we traverse the board left-to-right, we only need to check the piece to the right.
            if i % 6 != 5 and self.pos[i + 1] == piece:
                # Check for left-right moves. Since the current square is at the left endpoint,
                # we know to check immediately to the left for empty squares to move into.
                j = 1
                while (i % 6) - j >= 0 and self.pos[i - j] == 'o':
                    moves.append((piece, -j))
                    j += 1
                # Find the right endpoint of the piece, then check for rightward moves.
                offset = 1 + (i < 34 and self.pos[i + 2] == piece)
                j = 1
                while (i % 6) + j + offset <= 5 and self.pos[i + offset + j] == 'o':
                    moves.append((piece, j))
                    j += 1
            else:
                # Otherwise it must be an up-down piece, check for moves accordingly.
                j = 1
                while i - 6 * j >= 0 and self.pos[i - 6 * j] == 'o':
                    moves.append((piece, j))
                    j += 1
                # Find the bottom endpoint of the piece, then check for downward moves.
                offset = 1 + (i < 24 and self.pos[i + 12] == piece)
                j = 1
                while i + 6 * (j + offset) < 36 and self.pos[i + 6 * (j + offset)] == 'o':
                    moves.append((piece, -j))
                    j += 1
        return moves

    def doMove(self, move, **kwargs):
        if (
            not isinstance(move, tuple)
            or len(move) != 2
            or not isinstance(move[0], str)
            or not isinstance(move[1], int)
        ):
            raise TypeError
        if move not in self.generateMoves():
            raise ValueError
        new_pos = list(self.pos)
        # unpack move
        piece = move[0]
        i = self.pos.find(piece)
        n = move[1]
        # First check the piece's orientation to know which way to move
        if i % 6 != 5 and self.pos[i + 1] == piece:
            # Then find the piece length (only check to the right)
            length = 2 + (i < 34 and self.pos[i + 2] == piece)
            # Move the corresponding slice to the left or right
            new_pos[(i+n):(i+n+length)] = [piece] * length
            # Finally replace vacated spaces by o's
            if n > 0:
                new_pos[i:i+n] = ['o'] * n
            else:
                new_pos[i+length+n:i+length] = ['o'] * (-n)
        else:
            length = 2 + (i < 24 and self.pos[i + 12] == piece)
            # Here n > 0 means an upward move, which moves backwards in the array; so flip its sign for clarity
            n = -n
            new_pos[i+n*6:i+(length+n)*6:6] = [piece] * length
            if n > 0:
                new_pos[i:i+n*6:6] = ['o'] * n
            else:
                new_pos[i+(length+n)*6:i+length*6:6] = ['o'] * (-n)
        return Rush(variant_id=self.variant_id, pos=''.join(new_pos))


puzzle = Rush(variant_id=4)
TUI(puzzle, solver=GeneralSolver(puzzle), info=True).play()
# from scripts.server import test_puzzle
# test_puzzle(Rush)

