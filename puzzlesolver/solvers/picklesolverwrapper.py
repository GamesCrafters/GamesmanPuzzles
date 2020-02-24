import pickle
from . import GeneralSolver
from .solver import Solver
from pathlib import Path
from copy import deepcopy

class PickleSolverWrapper(Solver):

    def __init__(self, puzzle=None, path="./databases", solver=GeneralSolver):
        Path(path).mkdir(parents=True, exist_ok=True)
        assert puzzle
        try:
            f = open(path + "/" + puzzle.getName() + '.pkl', 'rb')
            self.solver = pickle.load(f)
            assert isinstance(self.solver, Solver)
            f.close()
        except FileNotFoundError:
            print("WARNING: File not found, intializing new memory storage")
            self.solver = solver()
            assert isinstance(self.solver, Solver), "Not a solver"
            self.solver.solve(puzzle)
            f = open(path + "/" + puzzle.getName() + ".pkl", 'wb')
            pickle.dump(self.solver, f)
            f.close()
        self.solve = self.solver.solve
        self.getRemoteness = self.solver.getRemoteness
        