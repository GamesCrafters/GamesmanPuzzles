# Introduction to Puzzles
Welcome to GamesmanPuzzles, the GamesCrafters group dedicated to the development and maintainence of `puzzlesolver`, a Python package made to define a general model for puzzles and for strongly solving them. 

Import the puzzlesolver package to access our functionality.
```python
>>> import puzzlesolver as ps  
```

## Puzzles
The base of the `puzzlesolver` package is the **Puzzle** model. Puzzles are logic problems that require certain sequences of Moves to end on a Puzzle solution. The fundamental goal of GamesmanPuzzles is to solve those Puzzles in the quickest way possible, which we achieve by creating **Solvers**. 

We implement our Puzzles using Abstract Base Classes and have subclasses that represent specific puzzles, like Towers of Hanoi and Cracker Barrel.

As an example, we'll be trying the Towers of Hanoi Puzzle:
```python
>>> puzzle = ps.puzzles.Hanoi()
>>> print(puzzle)
[[3, 2, 1], [], []]
```
Here, we have the default boardstate of a game of Towers of Hanoi. The nested lists represent rods to put the discs on, while the numbers represent each disk and their size. Leftmost numbers are on the bottom of the rod, while rightmost numbers are on top. 

Let's see what kind of moves we can make by executing `generateMoves()`
```python
>>> puzzle.generateMoves()
[(0, 1), (0, 2)]
```
Each entry of this list represents a possible move that we can make. In this Towers of Hanoi, the move `(0, 1)` represents moving the top disk from the first stack and placing that disc ontop of the second stack. 

Let's try to apply a move on this puzzle by calling `doMove()`.
```python
>>> moves = puzzle.generateMoves()
>>> newPuzzle = puzzle.doMove(moves[0])
>>> print(newPuzzle)
[[3, 2], [1], []]
```
As expected, the top disk of the first stack was moved onto the second stack.

## Solvers
The goal of GamesmanPuzzles is not just to make Puzzle models, but also solve them. We do this by creating solvers.

```python
>>> puzzle = ps.puzzles.Hanoi()
>>> solver = ps.solvers.GeneralSolver(puzzle) 
```
Here, we instantiated a subclass of the Solver object called GeneralSolver. GeneralSolver is an in-memory based solver that uses a Breath-First Search algorithm to traverse the [puzzle tree](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree). We can utilize it by running `solve()` and `getRemoteness()`.

```python
>>> solver.solve()
>>> solver.getRemoteness(puzzle)
7
```
**Remoteness** is defined to be the minimum number of moves needed to get from the current Puzzle to a Puzzle solution. If you can find the remoteness of all Puzzles, you can formulate a sequence of moves to reach a solution. This is what the GeneralSolver does.

If we move the top disk from the first stack to the last stack, which is move `(0, 2)`, for example:
```python
>>> print(puzzle)
[[3, 2, 1], [], []]
>>> moves = puzzle.generateMoves()
>>> moves
[(0, 1), (0, 2)]
>>> newPuzzle = puzzle.doMove(moves[1])
>>> print(newPuzzle)
[[3, 2], [], [1]]
>>> solver.getRemoteness(newPuzzle)
6
```
We can see that the remoteness of the nextPuzzle became 6, meaning there are 6 moves left until we reach the solution. 

As a member of GamesmanPuzzles, you are required to implement your own Puzzle. This [guide](00_Puzzle_Prerequisites.md) will help you implement your own Puzzle and Solver.