# Solver Prerequisites
This next part of the tutorial will teach you how to make a Solver object based on the Solver class. We'll be implementing the BFS algorithm GeneralSolver. This guide will assume that you are already familiar with Python 3 and that you have checked out the following documentation for a [puzzle tree](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree). This guide also assumes that you've followed the prerequisites of creating a Puzzle.

## Initialize files
Create a **NEW** Python file and import the following:
```python
from puzzlesolver.solvers.solver import Solver
from puzzlesolver.util import *
from puzzlesolver.puzzles.hanoi import Hanoi
from puzzlesolver.puzzleplayer import PuzzlePlayer
import queue as q
```

The rest of guide will implement the instance methods of this class.

[Next step: Helper Methods](5_Helper_Methods.md)
