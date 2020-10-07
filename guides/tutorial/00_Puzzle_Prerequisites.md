# Puzzle Prerequisites
This guide will teach you how to make a Puzzle object based on the Puzzle class. This guide will assume that you are already familiar with Python 3.

## Initialize files
Clone this repository and navigate into the base directory: 

```bash
git clone https://github.com/GamesCrafters/GamesmanPuzzles.git
cd GamesmanPuzzles
```

Make sure you installed all the dependencies! It's recommended to use a virtualenv for this:
```bash
pip install -r requirements.txt
```

Create a new Python file **in the GamesmanPuzzles directory** (making sure the dependencies are in the right location) and import the following:
```python
from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver import PuzzlePlayer
```

The rest of guide will implement the instance methods of this class.

[Next step: Gameplay Methods](01_Gameplay_Methods.md)
