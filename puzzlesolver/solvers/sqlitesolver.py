from . import GeneralSolver
from ..util import *

from sqlitedict import SqliteDict

class SqliteSolver(GeneralSolver):
    DATABASE_DIR = 'databases'

    def __init__(self, puzzle, *args, **kwargs):
        GeneralSolver.__init__(self, puzzle, *args, **kwargs)

    @property
    def path(self): 
        return '{}/{}.sqlite'.format(SqliteSolver.DATABASE_DIR, self.puzzle.getName())
        
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