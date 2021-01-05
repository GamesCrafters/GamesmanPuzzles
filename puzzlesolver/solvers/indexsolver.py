from collections.abc import MutableMapping
from .generalsolver import GeneralSolver
from functools import partial
import os

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
        self.path = '{}/{}{}.txt'.format(dir_path, puzzle.name, puzzle.variant)

    def getRemoteness(self, puzzle, *args, **kwargs):
        if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
        with open(self.path, 'r+b') as fo:
            fo.seek(hash(puzzle) * 2)
            chunk = fo.read(2)
            remote = int.from_bytes(chunk, byteorder='little') - 1
            return remote
        return PuzzleValue.UNSOLVABLE

    def solve(self, *args, overwrite=False, **kwargs):
        if overwrite or not os.path.exists(self.path):
            self._read()
            GeneralSolver.solve(self, *args, **kwargs)
            self._write()

    def _read(self):
        if not os.path.exists(self.path): open(self.path, 'w+')
        with open(self.path, 'r+b') as fo:
            cur_index = 0
            for chunk in iter(partial(fo.read, 2), b''):
                if chunk: 
                    self.remoteness[cur_index] = int.from_bytes(chunk, byteorder='little') - 1
                cur_index += 1

    def _write(self):
        ba = bytearray(2 * (max(self.remoteness) + 1))
        for i in self.remoteness:
            chunk = (self.remoteness[i] + 1).to_bytes(2, byteorder='little')
            ba[i * 2] = chunk[0]
            ba[i * 2 + 1] = chunk[1]
        with open(self.path, 'w+b') as fo:
            fo.write(ba)
