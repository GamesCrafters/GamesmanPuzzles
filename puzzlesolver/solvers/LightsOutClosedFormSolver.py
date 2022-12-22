from .solver import Solver
from ..util import *
import numpy as np
from sage.all import MatrixSpace, GF

class LightsOutClosedFormSolver(Solver):
    def __init__(self, puzzle, **kwargs):
        self.puzzle = puzzle
        self.path = ""
        
    def getRemoteness(self, puzzle, *args, **kwargs):
        m = int(puzzle.variant)
        n = m**2
        mat = self.__construct_matrix(m, m)
        MS = MatrixSpace(GF(2), n, n)
        A = MS(mat.flatten().tolist())
        A_inv = A.inverse()
        target = self.__construct_target(puzzle, n)
        res = A_inv@target
        return int(np.sum(res, dtype=int))
        
    def solve(self):
        pass

    @staticmethod
    def __construct_target(puzzle, n: int) -> np.array:
        h = hash(puzzle)
        target = np.zeros((n, 1), dtype=int)
        for i in range(n):
            target[i][0] = (h >> i) & 1
        return target

    @staticmethod
    def __construct_matrix(m: int, n: int) -> np.array:
        mat = np.zeros((m * n, m * n), dtype=int)
        for k in range(m * n):
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
        return mat
