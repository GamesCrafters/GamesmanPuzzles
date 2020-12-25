# What is Puzzlesolver?

**Puzzlesolver provides a simple but powerful API for solving Puzzles**

Puzzlesolver accomplishes this mission by:
- Providing the framework for Puzzles to be fit
- Offering a large range of Puzzles already fitted
- Providing powerful functionality to solve these Puzzles

## Getting Started with Puzzlesolver

Start by accessing an example Puzzle and Solver. Try out Hanoi for an example.

```python
from puzzlesolver.puzzles import Hanoi

puzzle = Hanoi() # Equivalent to Hanoi(variant={rod_variant : 3, disk_variant : 3})
print(puzzle) # [[0, 1, 2], [], []]
```
Tower of Hanoi (Hanoi for short) is a Puzzle that consists of rods and disks. Check out the [Wikipedia link](https://en.wikipedia.org/wiki/Tower_of_Hanoi) for more. The above code instantiated a Hanoi Puzzle boardstate with the default variant of 3 rods and 3 disks, however it can be instantiated with a different variant.

### The Puzzle boardstate

Once the Puzzle has been instantiated, the Puzzle boardstate is automatically set to a starting position of the Puzzle. In our Hanoi example, the starting boardstate is when the leftmost rod contains all of the disks. We can execute moves on the boardstate to move to another boardstate.

```python
print(puzzle) # [[0, 1, 2], [], []]
puzzle = puzzle.doMove([0, 1]) # Move from the first rod to the middle rod
print(puzzle) # [[0, 1], [2], []]
```
***Note that the `doMove` function is immutable, meaning that it instantiates a new Puzzle boardstate everytime its called.***

### The Solver

Next, start by solving the Puzzle using a Solver. We'll use GeneralSolver for this example. Instantiate the Solver with the Puzzle you wish to solve.
```python
from puzzlesolver.solvers import GeneralSolver

solver = GeneralSolver(puzzle)
```

The Solver is now ready to solve the Puzzle! Finish it off by executing `solve` on the Solver.
```python
solver.solve()
```

Finally, we are able to utilize the useful functions of the solver. We can access the remoteness of the Puzzle by calling `getRemoteness` on the solver to calculate the number of moves remaining

```python
print(puzzle) # [[0, 1], [2], []]
solver.getRemoteness(puzzle) # 8
```

## Creating your own Puzzle and Solver

This guide is meant for newcommers of the GamesmanPuzzles project to gain an intuition of how a Puzzle is solved by implementing the puzzle of Hanoi as well as the GeneralSolver. We'll first implement the Puzzle, and later implement the Solver. Start by looking at the [Puzzle prerequisites](00_Puzzle_Prerequisites.md).