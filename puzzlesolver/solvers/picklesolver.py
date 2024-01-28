from .generalsolver import GeneralSolver
import os
import pickle
import random
from ..util import *


class PickleSolver(GeneralSolver):
    """
    A persistence solver that places remoteness values into two-byte chunks, then
    saves them sequentially in a data file. The hash of the puzzle is used to determine
    the index of the chunk. Recommended for puzzles with tight hash functions.
    """

    def __init__(self, puzzle, *args, dir_path="databases", **kwargs):
        GeneralSolver.__init__(self, puzzle, *args, **kwargs)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.path = "{}/{}{}.pickle".format(dir_path, puzzle.id, puzzle.variant)
        self.solvableHashes = []

    def getRandomSolvableHash(self):
        if not self._remoteness:
            self._read()
        return random.choice(self.solvableHashes)

    def getRemoteness(self, puzzle, *args, **kwargs):
        if not self._remoteness:
            self._read()
        return GeneralSolver.getRemoteness(self, puzzle, *args, **kwargs)

    def solve(self, *args, overwrite=False, **kwargs):
        if overwrite or not os.path.exists(self.path):
            GeneralSolver.solve(self, *args, **kwargs)
            self._generateSolvableHashes()
            self._write()
        else:
            print(f'Database file {self.path} found! No need to re-solve.')
            #self._read()

    def _read(self):
        if not self._remoteness and os.path.exists(self.path):
            with open(self.path, "r+b") as fo:
                self._remoteness = pickle.load(fo)
            self._generateSolvableHashes()

    def _write(self):
        with open(self.path, "w+b") as fo:
            pickle.dump(self._remoteness, fo)

    def _generateSolvableHashes(self):
        assert(self._remoteness)
        self.solvableHashes = [key for key in self._remoteness.keys()
            if self._remoteness[key] >= 0 and self._remoteness[key] < PuzzleValue.MAX_REMOTENESS]
