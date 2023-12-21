# from collections.abc import MutableMapping
from .generalsolver import GeneralSolver
import os
import gzip
import random
from ..util import PuzzleValue
class IndexSolver(GeneralSolver):
    """
    A persistence solver that places remoteness values into two-byte chunks, then
    saves them sequentially in a data file. The hash of the puzzle is used to determine
    the index of the chunk. Recommended for puzzles with tight hash functions.
    """
    def __init__(self, puzzle, *args, dir_path='databases', **kwargs):
        GeneralSolver.__init__(self, puzzle, *args, **kwargs)
        if not os.path.exists(dir_path): os.makedirs(dir_path)
        self.path = '{}/{}{}.bin.gz'.format(dir_path, puzzle.id, puzzle.variant)
        self.ba = bytearray()
        self.solvableHashes = []
    
    def getRandomSolvableHash(self):
        if not self.solvableHashes:
            self._read()
        return random.choice(self.solvableHashes)

    def getRemoteness(self, puzzle, *args, **kwargs):
        if not self.ba:
            self._read()
        return self.ba[hash(puzzle)]

    def solve(self, *args, overwrite=False, **kwargs):
        if overwrite or not os.path.exists(self.path):
            self._read()
            GeneralSolver.solve(self, *args, **kwargs)
            self._write()
        else:
            print(f'Database file {self.path} found! No need to re-solve.')

    def _read(self):
        if not os.path.exists(self.path): open(self.path, 'wb').close()
        with gzip.open(self.path, 'rb') as fo:
            self.ba = fo.read()
            self.solvableHashes = [i for i in range(len(self.ba)) \
                if self.ba[i] < PuzzleValue.MAX_REMOTENESS and self.ba[i] >= 0]

    def _write(self):
        ba = bytearray(max(self._remoteness) + 1)
        for i in range(len(ba)):
            ba[i] = PuzzleValue.MAX_REMOTENESS
        for i in self._remoteness:
            chunk = self._remoteness[i].to_bytes(1, byteorder='little')
            ba[i] = chunk[0]
        with gzip.open(self.path, 'wb') as fo:
            fo.write(ba)
