from collections.abc import MutableMapping
from . import GeneralSolver
from functools import partial
import os

DATABASE_DIR = 'databases'

def readbytes(byte):
    return int.from_bytes(byte, byteorder='little')

class FODict(MutableMapping):
    def __init__(self, puzzle, *args, **kwargs):
        self.path = '{}/{}.txt'.format(DATABASE_DIR, puzzle.getName())
        if not os.path.exists(self.path): open(self.path, 'w+')

    def __getitem__(self, key):
        fo = open(self.path, 'r+b')
        fo.seek(key * 2)
        byte = fo.read(2)
        value = readbytes(byte)
        if not value: raise KeyError('Key not in dictionary')
        fo.close()
        return value - 1

    def __setitem__(self, key, value):
        assert isinstance(value, int)
        value += 1
        fo = open(self.path, 'r+b')
        fo.seek(key * 2)
        byte = (value).to_bytes(2, byteorder='little')
        fo.write(byte)
        fo.close()

    def __delitem__(self, key):
        self.__setitem__(key, 0)

    def __iter__(self):
        with open(self.path, 'r+b') as fo:
            for byte in iter(partial(fo.read, 2), b''):
                value = readbytes(byte)
                if value:
                    size += 1
                    yield value

    def __len__(self):
        return 1

    def __keytransform__(self, key):
        return key

class GZipSolver(GeneralSolver):

    def __init__(self, puzzle, *args, **kwargs):
        GeneralSolver.__init__(self, puzzle, *args, **kwargs)
        self.remoteness = FODict(puzzle)