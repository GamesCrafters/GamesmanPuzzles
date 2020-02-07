# Prerequisites:
This guide will teach you how to make puzzle object based on the puzzle class. This guide will assume that you are already familiar with Python 3.

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
from puzzlesolver.solver.GeneralSolver import GeneralSolver
from puzzlesolver.PuzzlePlayer import PuzzlePlayer
```

Initialize a new class object called Hanoi:
```python
class Hanoi:
```

The rest of guide will implement the instance methods of this class.

[Next step: Gameplay](Gameplay.md)
