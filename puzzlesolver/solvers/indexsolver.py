# from collections.abc import MutableMapping
from .generalsolver import GeneralSolver
from functools import partial
import os
import gzip

from ..util import *

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

    def getRemoteness(self, puzzle, *args, **kwargs):
        h = hash(puzzle)
        if h in self._remoteness:
            return self._remoteness[h]
        with gzip.open(self.path, 'rb') as fo:
            fo.seek(h)
            chunk = fo.read(1)
            remote = int.from_bytes(chunk, byteorder='little')
            return remote
        return float("inf")

    def solve(self, *args, overwrite=False, **kwargs):
        if overwrite or not os.path.exists(self.path):
            self._read()
            GeneralSolver.solve(self, *args, **kwargs)
            self._write()

    def _read(self):
        if not os.path.exists(self.path): open(self.path, 'wb').close()
        with gzip.open(self.path, 'rb') as fo:
            cur_index = 0
            for chunk in iter(partial(fo.read, 1), b''):
                if chunk: 
                    self._remoteness[cur_index] = int.from_bytes(chunk, byteorder='little')
                cur_index += 1

    def _write(self):
        ba = bytearray(max(self._remoteness) + 1)
        for i in self._remoteness:
            chunk = self._remoteness[i].to_bytes(1, byteorder='little')
            ba[i] = chunk[0]
        with gzip.open(self.path, 'wb') as fo:
            fo.write(ba)
