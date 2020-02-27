# Prerequisites:
This guide will teach you how to make a Solver object based on the Solver class. We'll be implementing the BFS algorithm GeneralSolver. This guide will assume that you are already familiar with Python 3 and that you have checked out the following documentation for a [puzzle tree](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree).

## Initialize files
Clone this repository and navigate into the base directory: 

```bash
git clone https://github.com/GamesCrafters/GamesmanPuzzles.git
cd GamesmanPuzzles
```

Create a new Python file and import the following:
```python
from puzzlesolver.solver.solver import Solver
from puzzlesolver.util import *
from puzzlesolver.puzzles.hanoi import Hanoi
from puzzlesolver.puzzleplayer import PuzzlePlayer
import queue as q
```

Initialize a new Solver object called GeneralSolver:
```python
class GeneralSolver(Solver):
```

The rest of guide will implement the instance methods of this class.

[Next step: Helper Methods](Helper.md)
