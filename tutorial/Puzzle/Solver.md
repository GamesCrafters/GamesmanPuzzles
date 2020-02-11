# Solver methods
Now that we have our own puzzle, it's time to solve it with our GeneralSolver! Using the Python file you developed in the [last step](Gameplay.md), we'll implement more instance functions in our Hanoi class so that the GeneralSolver can solve the puzzle.

## Solver functions
#### ```__hash__(self)```
This hash function allows the solver to use memoization to store previously computed values so that the solver doesn't require any other new computation. Hashes also must be unique such that no two "different" puzzle states have the same hash. Note that two unequal puzzle states do not necessarily have to be "different", as one puzzle state can simply be a variation (i.e. rotation, reflection) of the other state. This fact allows us to further optimize our solver to remove any redundant puzzle states. 

Our Hanoi puzzle will not be optimizing over redundant states and will simply just use the hash of the string representation of our stacks.
```python
def __hash__(self):
    return hash(str(self.stacks))
```

#### ```generateSolutions(self):```
The GeneralSolver is a bottom-top solver, meaning that it uses the endstates of the puzzle (when the puzzle has a "solvable" primitive) and solves from those positions. Because of that, the puzzle must compute the endstates of the puzzle itself. 

```python
def generateSolutions(self):
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
PuzzlePlayer(Hanoi(), solver=GeneralSolver()).play()
```
On your CLI, execute
```bash
python <your_python_file_name>.py
```
If you have a remoteness of 7 and a Primitive value of "SOLVABLE", congrats! You have successfully integrated the GeneralSolver into your game!

## Extras
Ponder on these questions in how we can optimize this puzzle
- If we change our endstate to be a stack on either the middle or right rod, how can we optimize this?
- Why is deserializing a hash to a puzzle a bad idea?

Also, check out the guide in creating a [Solver!](../)
