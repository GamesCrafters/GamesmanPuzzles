DATABASE_DIR = 'databases'

from .generalsolver import GeneralSolver
GSolver = GeneralSolver

from .sqlitesolver import SqliteSolver
SQLSolver = SqliteSolver

from .indexsolver import IndexSolver
ISolver = IndexSolver

from .picklesolver import PickleSolver
PSolver = PickleSolver

from .solver import Solver as _Solver