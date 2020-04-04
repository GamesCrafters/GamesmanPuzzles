from . import GeneralSolver
from ..util import *

from sqlitedict import SqliteDict

PATH = 'databases/'

class SqliteSolver(GeneralSolver):

    def __init__(self, puzzle, *args, path=PATH, **kwargs):
        GeneralSolver.__init__(self, puzzle, *args, **kwargs)
        self.path = '{}{}.sqlite'.format(path, puzzle.getName())

    def getRemoteness(self, puzzle, **kwargs):
        with SqliteDict(self.path) as self.remoteness:
            if str(hash(puzzle)) in self.remoteness:
                return self.remoteness[str(hash(puzzle))]
        return PuzzleValue.UNSOLVABLE

    def solve(self, *args, **kwargs):
        with SqliteDict(self.path) as self.remoteness:
            if self.puzzle.getName() not in self.remoteness:
                GeneralSolver.solve(self, *args, **kwargs)
                self.remoteness[self.puzzle.getName()] = 1
                self.remoteness.commit()