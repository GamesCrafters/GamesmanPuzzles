from . import GeneralSolver, DATABASE_DIR
from ..util import *
from pathlib import Path
from sqlitedict import SqliteDict

class SqliteSolver(GeneralSolver):
    """
    A persistence solver that uses sqlite databases as a way to store data
    """
    def __init__(self, puzzle, *args, dir_path='databases', **kwargs):
        GeneralSolver.__init__(self, puzzle, *args, **kwargs)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        self.database_path = dir_path

    @property
    def path(self): 
        return '{}/{}{}.sqlite'.format(
            self.database_path, self.puzzle.name, self.puzzle.variant)
        
    def getRemoteness(self, puzzle, **kwargs):
        with SqliteDict(self.path) as self.remoteness:
            if str(hash(puzzle)) in self.remoteness:
                return self.remoteness[str(hash(puzzle))]
        return PuzzleValue.UNSOLVABLE

    def solve(self, *args, **kwargs):
        with SqliteDict(self.path) as self.remoteness:
            if str(self.puzzle.variant) not in self.remoteness:
                GeneralSolver.solve(self, *args, **kwargs)
                self.remoteness[str(self.puzzle.variant)] = 1
                self.remoteness.commit()
