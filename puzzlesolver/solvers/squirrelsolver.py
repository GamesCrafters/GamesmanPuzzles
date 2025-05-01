from . import NoUndoSolver, DATABASE_DIR
from ..util import *
from pathlib import Path
from sqlitedict import SqliteDict

class SquirrelSolver(NoUndoSolver):
    """
    A persistence solver that uses sqlite databases as a way to store data
    """
    def __init__(self, puzzle, *args, dir_path='databases', **kwargs):
        NoUndoSolver.__init__(self, puzzle, *args, **kwargs)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        self.database_path = dir_path

    @property
    def path(self): 
        return '{}/{}{}.sqlite'.format(
            self.database_path, self.puzzle.id, self.puzzle.variant)
        
    def getRemoteness(self, puzzle, **kwargs):
        
        with SqliteDict(self.path) as self._remoteness:
            if str(hash(puzzle)) in self._remoteness:
                return self._remoteness[str(hash(puzzle))]
        return 127

    def solve(self, *args, **kwargs):
        with SqliteDict(self.path) as self._remoteness:
            if str(self.puzzle.variant) not in self._remoteness:
                NoUndoSolver.solve(self, *args, **kwargs)
                self._remoteness[str(self.puzzle.variant)] = 1
                self._remoteness.commit()
