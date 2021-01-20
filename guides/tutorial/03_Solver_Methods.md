# Solver methods
Now that we have our own puzzle, it's time to solve it with our GeneralSolver! Using the Python file you developed in the [last step](Gameplay.md), we'll implement more instance functions in our Hanoi class so that the GeneralSolver can solve the puzzle.

## Solver functions
#### ```__hash__(self)```
This hash function allows the solver to use memoization to store previously computed values so that the solver doesn't require any other new computation. Hashes also must be unique such that no two "different" puzzle states have the same hash. Note that two unequal puzzle states do not necessarily have to be "different", as one puzzle state can simply be a variation (i.e. rotation, reflection) of the other state, or equivalently, **both puzzles have the same remoteness**. This fact allows us to further optimize our solver to remove any redundant puzzle states. 

Our Hanoi puzzle will not be optimizing over redundant states and will simply just use the hash of the string representation of our stacks.
```python
def __hash__(self):
    from hashlib import sha1
    h = sha1()
    h.update(str(self.stacks).encode())
    return int(h.hexdigest(), 16)
```

#### ```generateSolutions(self, **kwargs):```
The GeneralSolver is a bottom-top solver, meaning that it uses the endstates of the puzzle (when the puzzle has a "solvable" primitive) and solves from those positions. 

**Note: The GeneralSolver does not need this function defined.** Situations like this can occur in cases where there exists no efficient method of enumerating all "solvable" positions, but performance can be improved by pre-calculating an iterable of solved states in the generateSolutions function. In this case, there exists a single solved position, so we can efficiently enumerate all solved positions. 

```python
def generateSolutions(self, **kwargs):
    newPuzzle = Hanoi()
    newPuzzle.stacks = [
        [],
        [],
        [3, 2, 1]
    ]
    return [newPuzzle]
```

### Execute
Once you have implemented all the required functions, change the last line of the Python file outside of the class to:
```python
puzzle = Hanoi()
TUI(puzzle, solver=GeneralSolver(puzzle), info=True).play()
```
On your CLI, execute
```bash
python <your_python_file_name>.py
```
If you have a remoteness of 7 and a Primitive value of "UNDECIDED", congrats! You have successfully integrated the GeneralSolver into your game!

## Extras
Ponder on these questions in how we can optimize this puzzle
- If we change our endstate to be a stack on either the middle or right rod, how can we optimize this?
- If you can compute a hash that directly encodes the remoteness, is there a need for a solver?

[Next Part: Implementing a Solver](04_Solver_Prerequisites.md)
