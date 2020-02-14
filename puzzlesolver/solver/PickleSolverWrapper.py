import pickle
from .GeneralSolver import GeneralSolver
import os

class PickleSolverWrapper(GeneralSolver):

    def __init__(self, puzzle=None, path="."):
        try:
            assert puzzle
            f = open(path + "/" + puzzle.__class__.__name__ + '.pkl', 'rb')
            pkl = pickle.load(f)
            self.values, self.remoteness = pkl[0], pkl[1]
            f.close()
        except FileNotFoundError:
            print("WARNING: File not found, intializing new memory storage")
            GeneralSolver.__init__(self, puzzle=puzzle)
        self.path = path

    def solve(self, puzzle):
        output = GeneralSolver.solve(self, puzzle)
        f = open(self.path + "/" + puzzle.__class__.__name__ + ".pkl", 'wb')
        pickle.dump([self.values, self.remoteness], f)
        f.close()
        return output
