DATABASE_DIR = 'databases'

from .generalsolver import GeneralSolver
from .sqlitesolver import SqliteSolver
from .picklesolverwrapper import PickleSolverWrapper
from .gzipsolver import GZipSolver
from .solver import Solver