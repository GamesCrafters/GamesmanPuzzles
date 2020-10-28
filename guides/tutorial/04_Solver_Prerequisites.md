# Solver Prerequisites
This next part of the tutorial will teach you how to make a custom solver following the Solver interface. We'll be implementing the in memory BFS algorithm GeneralSolver. This guide will assume that you are already familiar with Python 3 and that you have checked out the following documentation for a [puzzle tree](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree). This guide also assumes that you've followed the prerequisites of creating a Puzzle.

## Initialize files
Create a **NEW** Python file and import the following:
```python
from puzzlesolver.util import *
from puzzlesolver.solvers import Solver
from puzzlesolver.puzzles import Hanoi
from puzzleplayer import PuzzlePlayer
import queue as q
```

The rest of guide will implement the instance methods of this class.

[Next step: Helper Methods](05_Helper_Methods.md)
