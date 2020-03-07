# Miscellaneous Functions
Our GeneralSolver uses a bottom to top BFS algorithm to classify positions of the puzzle. This guide assumes that you have checked out the following documentation for a [puzzle tree.](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree)

The following steps define functions to initialize the Solver object, as well as getting remoteness of the Puzzle after solving.

Initialize a new Solver object called GeneralSolver:
```python
class GeneralSolver(Solver):
```

## Implementing Functions

**```__init__(self, **kwargs)```**

We initialize the dictionaries used to store the values and remoteness of the positions.

```python
def __init__(self, **kwargs):
    self.values = {}
    self.remoteness = {}
```

**```getRemoteness(self, puzzle, **kwargs)```**

This is just a function used to help the PuzzlePlayer find the remoteness of the position
```python
def getRemoteness(self, puzzle, **kwargs):
    self.solve(puzzle)
    if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
    return PuzzleValue.UNSOLVABLE
```

[Next Step: Implementing the Solver Methods](6_Solver_Methods.md)