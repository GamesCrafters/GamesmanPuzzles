from re import L
from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI

class Demo(ServerPuzzle):
    id = 'demo'
    variants = ['4_bi', '3_bi', '4_for']

    def __init__(self, start = 4, variant = None, **kwargs):
        self._start = start
        self._pos = self._start
        s, mt = variant.split('_')
        self._variant = variant
        self._movetype = mt

    def toString(self, mode):
        if mode == StringMode.AUTOGUI: 
            return f'1_{self._pos}'
        return str(self._pos)

    def primitive(self, **kwargs):
        if self._pos == 0: 
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype='all'):
        # if self._pos == 0:
        #     return []
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
        nP = Demo(start=self._start, variant=self._variant)
        position = self._pos
        position -= move[0]
        nP._pos = position
        return nP
    
    def moveString(self, move, mode):
        return f"Move {move[0]}"

    def __hash__(self):
        return self._pos

    @property
    def variant(self):
        """Override the parent's read-only property with our own."""
        return self._variant

    @variant.setter
    def variant(self, val):
        """This setter lets us do self.variant = <something>."""
        self._variant = val

    @property
    def variant(self):
        """Override the parent's read-only property with our own."""
        return self._variant

    @variant.setter
    def variant(self, val):
        """This setter lets us do self.variant = <something>."""
        self._variant = val

    @classmethod
    def generateStartPosition(cls, variant_id):
        start_pos, movetype = variant_id.split('_')
        return cls(start=int(start_pos), variant=variant_id)

    @classmethod
    def fromString(cls, variant_id, position_str):
        if position_str == "":
            return cls.generateStartPosition(variant_id)
        try:
            start_pos, movetype = variant_id.split('_')
            curr_pos, _ = position_str.split("_")
            pos = int(curr_pos)
            puzzle = cls(start=int(start_pos), variant=variant_id)
            puzzle._pos = pos
            return puzzle
        except ValueError:
            raise ValueError("Position string must be an integer")
# TUI(Demo()).play()
