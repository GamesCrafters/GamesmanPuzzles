import os
from ctypes import *
from puzzlesolver.puzzles import Hanoi
import time

lib = PyDLL("./bin/libsolver.so")
init = lib.init
init.restype = c_void_p

setRemoteness = lib.setRemoteness
setRemoteness.argtypes = [ c_void_p, c_int, c_int ]

getRemoteness = lib.getRemoteness
getRemoteness.argtypes = [ c_void_p, c_int ]

ptr = init()
print("Setting: ", setRemoteness(ptr, 2, 2))
print("Getting: ", getRemoteness(ptr, 2))