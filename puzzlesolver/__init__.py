from . import python
import sys

# Renaming package names to avoid doing "import puzzlesolver.python.puzzles"
sys.modules["puzzlesolver.puzzles"] = python.puzzles
sys.modules["puzzlesolver.solvers"] = python.solvers
sys.modules["puzzlesolver.util"]    = python.util