# Puzzle Prerequisites:
This guide will teach you how to make  a Puzzle object based on the Puzzle class. This guide will assume that you are already familiar with Python 3.

## Initialize files
Clone this repository and navigate into the base directory: 

```bash
git clone https://github.com/GamesCrafters/GamesmanPuzzles.git
cd GamesmanPuzzles
```

Create a new Python file and import the following:
```python
from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles.puzzle import Puzzle
from puzzlesolver.solvers.generalsolver import GeneralSolver
from puzzlesolver.puzzleplayer import PuzzlePlayer
```

The rest of guide will implement the instance methods of this class.

[Next step: Gameplay Methods](1_Gameplay_Methods.md)