from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI

class Demo2(ServerPuzzle):
    id = 'demo2'
    variants = ['4', '3']

    def __init__(self, start = 4, variant = None, **kwargs):
        self._start = start
        self._pos = self._start
        self._variant = variant

    def toString(self, mode):
        if mode == StringMode.AUTOGUI: 
            return f'1_{self._pos}'
        return str(self._pos)

    def primitive(self, **kwargs):
        if self._pos == 0: 
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateMoves(self, movetype='all'):
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
        nP = Demo2(start=self._start, variant=self._variant)
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

    @classmethod
    def generateStartPosition(cls, variant_id):
        return cls(start=int(variant_id), variant=variant_id)

    @classmethod
    def fromString(cls, variant_id, position_str):
        try:
            pos = int(position_str)
            puzzle = cls(start=int(variant_id), variant=variant_id)
            puzzle._pos = pos
            return puzzle
        except ValueError:
            raise ValueError("Position string must be an integer")
