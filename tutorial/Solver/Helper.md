# Miscellaneous Functions
Our GeneralSolver uses a bottom to top BFS algorithm to classify positions of the puzzle. This guide assumes that you have checked out the following documentation for a [puzzle tree.](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree)

## Implementing functions

**```__init__(self)```**

We initialize the dictionaries used to store the values and remoteness of the positions.

```python
def __init__(self, *args, **kwargs):
    self.values = {}
    self.remoteness = {}
```

**```getRemoteness(self)```**

This is just a function used to help the PuzzlePlayer find the remoteness of the position
```python
def getRemoteness(self, puzzle):
    self.solve(puzzle)
    if hash(puzzle) in self.remoteness: return self.remoteness[hash(puzzle)]
    return PuzzleValue.UNSOLVABLE
```

[Next Step: Implementing the Solver](Solver.md)