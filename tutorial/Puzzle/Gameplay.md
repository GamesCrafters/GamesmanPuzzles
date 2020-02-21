# Gameplay Methods
<p align="center">
<img src='Tower_of_hanoi.jpeg'>
</p>

Hanoi is a commonly known and simple puzzle. The puzzle consists of three rods and a stack of differently sized rings on one rod. The goal is to take a stack of rings and move them one by one to form another stack of rings on the rightmost rod. The only restriction is that a bigger ring cannot be on top of a smaller ring.

The goal of this step is to explain the functionality for the GamesmanPuzzles version of Hanoi as well as implement the functions so that we'll be able to interact with it on our PuzzlePlayer. This document assumes you have satisfied the [prerequisties](Prerequisites.md). 
## Gameplay functions
#### `__init__(self)`
We want to initialize our puzzle with its starting position. For Hanoi, our starting position is a stack of discs on the leftmost rod. For this example, we will represent the rods with a list of lists containing integers, which represent the size of the disc. Also, the order of the integers from left to right, represents the order of the discs from bottom to top.
```python
def __init__(self):
    self.stacks = [[3, 2, 1], [], []]
```
#### `__str__(self)`
The string representation of the puzzle will help visualize the state of our stacks on our PuzzlePlayer interface. For a quick visual, we'll be using the string representation of the lists we used.
```python
def __str__(self):
    return str(self.stacks)
```
#### `primitive(self)`
The primitive of the puzzle describes if the puzzle has reached the solution or not. If it has reached the endstate, we will a arbitrary value that we define as SOLVABLE. Otherwise, it's considered to be UNDECIDED. For our version of Hanoi, a SOLVABLE primitive would be when 
```python
def primitive(self):
    if self.stacks[2] == [3, 2, 1]:
        return PuzzleValue.SOLVABLE
    return PuzzleValue.UNDECIDED
```
#### `generateMoves(self)`
This function allows the puzzle to generate possible moves and move the puzzle forward. It should return all possible moves (including undos) that any player can make on the puzzle. For Hanoi, a move is to move the top piece of any rod onto another rod as long as it satisfies the restriction that a bigger ring cannot be on top of a smaller ring.

**Note:** We also have to include "undo" moves, which are moves that may not technically be legal (i.e. undoing a move in Chess could be uncapturing a piece or a pawn moving backwards). We need these moves as our GeneralSolver moves from the end state to the start states. Consider if undoing any move is a legal move in your puzzle and if it isn't, implement `generateLegalMoves(self)` as well, which returns a list of legal moves.  
```python
def generateMoves(self):
    moves = []
    for i, stack1 in enumerate(self.stacks):
        if not stack1: continue
        for j, stack2 in enumerate(self.stacks):
            if i == j: continue
            if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
    return moves
```



#### `doMove(self, move)`
Do move produces a puzzle after the move was executed onto the puzzle. It's important to generate an entirely new game with the move executed so that it works with the solver (which we will delve into later). 
```python
def doMove(self, move):
    newPuzzle = Hanoi()
    stacks = deepcopy(self.stacks)
    stacks[move[1]].append(stacks[move[0]].pop())
    newPuzzle.stacks = stacks
    return newPuzzle
```
### Execute
Once you have implemented all the required functions, add a line on the end of the file outside the Hanoi class to execute the PuzzlePlayer. 
```python
PuzzlePlayer(Hanoi()).play()
```
On your CLI, execute
```bash
python <your_python_file_name>.py
```
If everything runs smoothly, congrats! You have created a playable puzzle!

[Next step: Implementing the Solver methods](Solver.md)
