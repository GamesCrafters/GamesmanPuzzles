import pickle
from .GeneralSolver import GeneralSolver

class PickleSolverWrapper(GeneralSolver):

    def __init__(self, puzzle=None):
        try:
            assert puzzle
            f = open(puzzle.__class__.__name__ + '.pkl')
            pkl = pickle.load(f)
            self.values, self.remoteness = pkl[0], pkl[1]
            f.close()
        except:
            print("WARNING: Error opening file")
            GeneralSolver.__init__(self, puzzle=puzzle)

    def solve(self, puzzle):
        output = GeneralSolver.solve(self, puzzle)
        f = open(puzzle.__class__.__name__ + ".pkl", 'wb')
        pickle.dump([self.values, self.remoteness], f)
        f.close()
        return output
