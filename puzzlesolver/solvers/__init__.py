DATABASE_DIR = 'databases'

from .generalsolver import GeneralSolver
GSolver = GeneralSolver

from .undosolver import NoUndoSolver
UndoSolver = NoUndoSolver

from .sqlitesolver import SqliteSolver
SQLSolver = SqliteSolver

from .indexsolver import IndexSolver
ISolver = IndexSolver

from .picklesolver import PickleSolver
PSolver = PickleSolver

from .lightsoutclosedformsolver import LightsOutClosedFormSolver
LOCFSolver = LightsOutClosedFormSolver

from .no_undo_solver import NoUndoSolver
NoUndo = NoUndoSolver

from .squirrelsolver import SquirrelSolver

from .solver import Solver as _Solver
