DATABASE_DIR = 'databases'

from .solver import Solver as _Solver
from .generalsolver import GeneralSolver
from .picklesolver import PickleSolver
from .indexsolver import IndexSolver
from .sqlitesolver import SqliteSolver
from .mpisolver import MPISolver


GSolver = GeneralSolver

SQLSolver = SqliteSolver

ISolver = IndexSolver

PSolver = PickleSolver
