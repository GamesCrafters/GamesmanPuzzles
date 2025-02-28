from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI

class Demo(ServerPuzzle):
    id = 'demo'
    variants = ['4_bi', '10_bi', '4_for']

    def __init__(self, start=4, variant=None, **kwargs):
        self._start = start
        self._pos = start
        s, mt = variant.split('_')  # e.g. "4_for" => s="4", mt="for"
        self._variant = variant
        self._movetype = mt

    def toString(self, mode):
        if mode == StringMode.AUTOGUI:
            return f'1_{self._pos}'
        return str(self._pos)

    def primitive(self, **kwargs):
        """Classify terminal positions."""
        if self._pos == 0:
            return PuzzleValue.SOLVABLE  # "win"
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype):
        # if self._pos == 0:
        #     return []
        # if self.primitive() != PuzzleValue.UNDECIDED:
        #     return []
        if self._movetype == 'for':
            return self._forward()
        else:
            return self._bidirectional()
    
    def _forward(self):
        """Forward-only moves: no negative deltas."""
        if self._pos % 3 == 0:
            return []
        if self._pos == 1:
            return [(1,)]
        elif self._pos % 4 == 1:
            return [(1,)]
        return [(2,), (1,)]
        # if self._pos != 0 and self._pos % 3 == 0:
        #     return []
        # if self._pos >= self._start:
        #     return [(1,), (2,)]
        # if (self._pos + 2) % 3 == 0:
        #     return [(-1,), (1,)] if self._pos % 4 == 1 else [(-1,), (1,), (2,)]
        # elif (self._pos + 1) % 3 == 0:
        #     return [(-2,), (1,)] if self._pos % 4 == 1 else [(-2,), (1,), (2,)]
        # return [(-2,), (-1,), (1,), (2,)]
    
    def _bidirectional(self):
        """Your original negative/positive moves logic."""
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
        """Create a new Demo puzzle with updated position."""
        nP = Demo(start=self._start, variant=self._variant)
        nP._pos = self._pos - move[0]
        return nP
    
    def moveString(self, move, mode):
        return f"Move {move[0]}"

    def __hash__(self):
        # If you plan to use an IndexSolver, ensure pos is in range or handle offset.
        return self._pos

    @property
    def variant(self):
        return self._variant

    @variant.setter
    def variant(self, val):
        self._variant = val

    @classmethod
    def generateStartPosition(cls, variant_id):
        return cls(start=int(variant_id.split('_')[0]), variant=variant_id)

    @classmethod
    def fromString(cls, variant_id, position_str):
        if position_str == "":
            return cls.generateStartPosition(variant_id)
        try:
            start_pos, movetype = variant_id.split('_')
            pos = int(position_str)
            puzzle = cls(start=int(start_pos), variant=variant_id)
            puzzle._pos = pos
            return puzzle
        except ValueError:
            raise ValueError("Position string must be an integer")

# TUI(Demo(variant="4_for")).play()
