import os
from ctypes import *
from puzzlesolver.puzzles import Hanoi
import time

lib = PyDLL("./libsolver.so")
solve = lib.solve
solve.argtypes = [ py_object ]

getRemoteness = lib.getRemotenessPyObject
getRemoteness.argtypes = [ py_object ]

print("Solving   : ", solve(Hanoi()))
print("Counting  : ", lib.getCount())
print("Checking  : ", getRemoteness(Hanoi()))
