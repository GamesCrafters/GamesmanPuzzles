from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI


class Demo(ServerPuzzle):
    # Example variants could be ['4_bi', '4_for', '3_bi']
    # meaning start=4, bidirectional or start=4, forward-only, etc.

    id = "demo"
    variants = ["4_bi", "4_for"]

    def __init__(self, start=4, movetype='for', variant=None, **kwargs):
        self._start = start
        self._pos = self._start
        self._movetype = movetype   # <-- store the move type
        self._variant = variant

    def toString(self, mode):
        if mode == StringMode.AUTOGUI:
            possible_moves = [(-2,), (-1,), (1,), (2,)]
            valid = self.generateMoves()
            bits = ''.join('1' if m in valid else '0' for m in possible_moves)
            return f'1_{self._pos}{bits}'
        else:
            return str(self._pos)

    def primitive(self, **kwargs):
        if self._pos == 0: 
            return PuzzleValue.SOLVABLE
        elif self._pos % 3 == 0 and self._pos != 0 and self._movetype == 'for':
            return PuzzleValue.UNSOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype='all'):
        """
        Now you can switch logic based on self._movetype:
        e.g. if 'for' means only forward moves, do that.
             if 'bi' means forward/backward, do your original logic.
        """
        if self._pos == 0:
            return []
        if self._movetype == 'for':
            if movetype in ('undo', 'back'):
                return []
            elif self._pos % 3 == 0:
                return []
            if self._pos % 4 == 1 and self._pos != 1:
                return [(2,)]
            elif self._pos == 1:
                return [(1,)]
            else:
                return [(1,), (2,)]
        else:
            if self._pos != 0 and self._pos % 3 == 0:
                return [(-1,)]
            elif self._pos >= self._start:
                return [(1,), (2,)]
            if (self._pos + 2) % 3 == 0:
                return [(-1,), (1,)] if self._pos % 4 == 1 else [(-1,), (1,), (2,)]
            elif (self._pos + 1) % 3 == 0:
                return [(-2,), (1,)] if self._pos % 4 == 1 else [(-2,), (1,), (2,)]
            return [(-2,), (-1,), (1,), (2,)]

    def doMove(self, move, **kwargs):
        """
        Should error check move to see if in valid format before exectuing move.
        """
        nP = Demo(start=self._start, movetype=self._movetype, variant=self._variant)
        position = self._pos
        position -= move[0]
        nP._pos = position
        return nP
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            delta = move[0]
            if delta == -2:
                center_index = 5
            elif delta == -1:
                center_index = 6
            elif delta == 1:
                center_index = 7
            else:  # 2
                center_index = 8
            return f"A_t_{center_index}_x"
        else:
            return f"Move {move[0]}"

    def __hash__(self):
        return self._pos + 1000

    @property
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, val):
        self._variant = val

    @classmethod
    def generateStartPosition(cls, variant_id):
        """
        Parse the variant string (e.g. '4_bi') => start=4, movetype='bi'.
        Then build the puzzle.
        """
        # Safely parse the variant, assuming it's always "<start>_<movetype>".
        start_str, movetype = variant_id.split('_')
        start = int(start_str)
        puzzle = cls(start=start, movetype=movetype, variant=variant_id)
        return puzzle

    @classmethod
    def fromString(cls, variant_id, position_str):
        """
        Also parse the variant string. If position_str is empty, start fresh.
        Otherwise parse the position from the string.
        """
        start_str, movetype = variant_id.split('_')
        start = int(start_str)

        if position_str == "":
            # Fresh start
            return cls(start=start, movetype=movetype, variant=variant_id)

        try:
            pos = int(position_str)
            puzzle = cls(start=start, movetype=movetype, variant=variant_id)
            puzzle._pos = pos
            return puzzle
        except ValueError:
            raise ValueError("Position string must be an integer")


# TUI(Demo()).play()
