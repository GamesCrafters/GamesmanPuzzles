import os
from ctypes import *
from puzzlesolver.puzzles import Hanoi
import time

lib = PyDLL("./bin/libsolver.so")
init = lib.init
init.restype = c_void_p

setRemoteness = lib.setRemotenessPyObject
setRemoteness.argtypes = [ c_void_p, py_object, c_int ]

getRemoteness = lib.getRemotenessPyObject
getRemoteness.argtypes = [ c_void_p, py_object ]

solve = lib.solve
solve.argtypes = [ c_void_p, py_object ]

clear = lib.clear
clear.argtypes = [ c_void_p ]

ptr = init()
print("Init     : ", ptr)
print("Solve    : ", solve(ptr, Hanoi()))
print("Getting  : ", getRemoteness(ptr, Hanoi()))
print("Clearing : ", clear(ptr))