DATABASE_DIR = 'databases'

from .generalsolver import GeneralSolver
GSolver = GeneralSolver

from .sqlitesolver import SqliteSolver
SQLSolver = SqliteSolver

from .indexsolver import IndexSolver
ISolver = IndexSolver

from .solver import Solver as _Solver