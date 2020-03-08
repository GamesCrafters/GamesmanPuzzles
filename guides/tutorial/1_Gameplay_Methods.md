# Gameplay Methods
<p align="center">
<img src='assets/Tower_of_hanoi.jpeg'>
</p>

Hanoi is a commonly known and simple puzzle. The puzzle consists of three rods and a stack of differently sized rings on one rod. The goal is to take a stack of rings and move them one by one to form another stack of rings on the rightmost rod. The only restriction is that a bigger ring cannot be on top of a smaller ring.

The goal of this step is to explain the functionality for the GamesmanPuzzles version of Hanoi as well as implement the functions so that we'll be able to interact with it on our PuzzlePlayer. 

Initialize a new Puzzle object called Hanoi:
```python
class Hanoi(Puzzle):
```

The rest of guide will implement the instance methods of this class.

## Gameplay functions
#### `__init__(self, **kwargs)`
We want to initialize our puzzle with its starting position. For Hanoi, our starting position is a stack of discs on the leftmost rod. For this example, we will represent the rods with a list of lists containing integers, which represent the size of the disc. Also, the order of the integers from left to right, represents the order of the discs from bottom to top.
```python
def __init__(self, **kwargs):
    self.stacks = [[3, 2, 1], [], []]
```
#### `__str__(self, **kwargs)`
The string representation of the puzzle will help visualize the state of our stacks on our PuzzlePlayer interface. For a quick visual, we'll be using the string representation of the lists we used.
```python
def __str__(self):
    return str(self.stacks)
```
#### `primitive(self, **kwargs)`
The primitive of the puzzle describes if the puzzle has reached the solution or not. If it has reached the endstate, we will a arbitrary value that we define as SOLVABLE. Otherwise, it's considered to be UNDECIDED. For our version of Hanoi, a SOLVABLE primitive would be when 
```python
def primitive(self, **kwargs):
    if self.stacks[2] == [3, 2, 1]:
        return PuzzleValue.SOLVABLE 
    return PuzzleValue.UNDECIDED
```
#### `doMove(self, move, **kwargs)`
Do move produces a puzzle after the move was executed onto the puzzle. It's important to generate an entirely new game with the move executed so that it works with the solver (which we will delve into later). 
```python
def doMove(self, move, **kwargs):
    if move not in self.generateMoves(): raise ValueError
    newPuzzle = Hanoi()
    stacks = deepcopy(self.stacks)
    stacks[move[1]].append(stacks[move[0]].pop())
    newPuzzle.stacks = stacks
    return newPuzzle        
```
[Next step: Implementing generateMoves](2_Moves.md)
