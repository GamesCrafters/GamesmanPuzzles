try:
    from sage.all import *
except ImportError:
    raise ValueError("Sage does not seem to be installed in this system. Please visit www.sagemath.org to fix this!")
from .solver import Solver
from ..util import *

class LightsOutClosedFormSolver(Solver):
    def __init__(self, puzzle, **kwargs):
        self.puzzle = puzzle
        self.path = "closed_form"
        
    def getRemoteness(self, puzzle, *args, **kwargs):
        m = int(puzzle.variant)
        op = self.__construct_matrix(m, m)
        # We cannot use python built-in hash() function here because
        # it truncates some hashes for variants >= 8.
        target = vector([int(val) for row in puzzle.grid for val in row])
        res = (op.inverse())*target
        return int(sum(vector(ZZ, res)))
        
    def solve(self):
        return

    @staticmethod
    def __construct_matrix(m: int, n: int):
        d = m * n
        mat = [[0 for _ in range(d)] for _ in range(d)]
        for k in range(d):
            i = k // n
            j = k % n
            mat[k][k] = 1
            # toggle left cell if possible
            if j > 0:
                mat[k-1][k] = 1
            # toggle right cell if possible
            if j < n - 1:
                mat[k+1][k] = 1
            # toggle cell above if possible
            if i > 0:
                mat[k-n][k] = 1
            # toggle cell below if possible
            if i < m - 1:
                mat[k+n][k] = 1
        return MatrixSpace(GF(2), d, d)(mat)
