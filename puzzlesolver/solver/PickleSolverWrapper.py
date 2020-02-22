import pickle
from .GeneralSolver import GeneralSolver
from pathlib import Path

class PickleSolverWrapper(GeneralSolver):

    def __init__(self, puzzle=None, path="."):
        Path(path).mkdir(parents=True, exist_ok=True)
        try:
            assert puzzle
            f = open(path + "/" + puzzle.getName() + '.pkl', 'rb')
            pkl = pickle.load(f)
            self.values, self.remoteness = pkl[0], pkl[1]
            f.close()
        except FileNotFoundError:
            print("WARNING: File not found, intializing new memory storage")
            GeneralSolver.__init__(self, puzzle=puzzle)
        self.path = path

    def solve(self, puzzle):
        if self.values and self.remoteness: return GeneralSolver.solve(self, puzzle)
        output = GeneralSolver.solve(self, puzzle)
        f = open(self.path + "/" + puzzle.getName() + ".pkl", 'wb')
        pickle.dump([self.values, self.remoteness], f)
        f.close()
        return output
