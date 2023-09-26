import random
from .solver import Solver
from ..util import *

try:
    from ..extern import m4ri_utils
except:
    class LightsOutClosedFormSolver(Solver):
        pass
else:
    class LightsOutClosedFormSolver(Solver):
        def __init__(self, puzzle, **kwargs):
            self.puzzle = puzzle
            self.path = "closed_form"
            self.op = [self.__construct_matrix(i, i) for i in range(9)]
            full_rank_variants = {2, 3, 6, 7, 8}
            for variant in full_rank_variants:
                self.op[variant] = m4ri_utils.mat_inv_GF2(self.op[variant])

        def getRandomSolvableHash(self):
            # All hashes are solvable if this closed-form solver can be used.
            return random.getrandbits(self.puzzle.size**2)

        def getRemoteness(self, puzzle, *args, **kwargs):
            m = int(puzzle.variant)
            op = self.op[m]
            # We cannot use python built-in hash() function here because
            # it truncates some hashes for variants >= 8.
            target = [[int(val)] for row in puzzle.grid for val in row]
            res = m4ri_utils.mat_mul_GF2(op, target)
            count = 0
            for i in range(m * m):
                count += res[i][0]
            return count

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
                    mat[k - 1][k] = 1
                # toggle right cell if possible
                if j < n - 1:
                    mat[k + 1][k] = 1
                # toggle cell above if possible
                if i > 0:
                    mat[k - n][k] = 1
                # toggle cell below if possible
                if i < m - 1:
                    mat[k + n][k] = 1
            return mat
