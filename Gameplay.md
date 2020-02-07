# Gameplay
Hanoi is a commonly known and simple puzzle. The puzzle consists of three rods and a stack of differently sized rings on one rod. The goal is to take a stack of rings and move them one by one to form another stack of rings on a different rod. The only restriction is that a bigger ring cannot be on top of a smaller ring.

The goal of this step is to implement functions for our Hanoi so that we'll be able to play it on our PuzzlePlayer. The Hanoi implemented in this step may not be  This document assumes you have satisfied the [prerequisties](). 
## Gameplay functions
### `__init__(self)`
We want to initialize our puzzle with its starting position. For Hanoi, our starting position is a stack of discs on the leftmost rod. For this example, we will represent the rods with a list of lists containing integers, which represent the size of the disc. Also, the order of the integers from left to right, represents the order of the discs from bottom to top.
```python
def __init__(self):
    self.board = [[3, 2, 1], [], []]
```
### `__str__(self)`
The string representation of the puzzle will help visualize the state of the board on our interface. For a quick visual, we'll be using the string representation of the lists we used.
```python
def __str__(self):
    return str(self.board)
```
### `primitive(self)`
The primitive of the puzzle describes if the puzzle has reached the solution or not. If it has reached the endstate, we will a arbitrary value that we define as SOLVABLE. Otherwise, it's considered to be UNDECIDED. 
```python
def primitive(self):
    if self.board[2] == [3, 2, 1]:
        return PuzzleValue.SOLVABLE
    return PuzzleValue.UNDECIDED
```
### `generateMoves(self)`
This function allows the puzzle to generate possible moves and move the puzzle forward. It should return all possible legal moves that any player can make on the puzzle. For Hanoi, a legal move is to move the top piece of any rod onto another rod as long as it satisfies the restriction that a bigger ring cannot be on top of a smaller ring.
```python
def generateMoves(self):
    moves = []
    for i, rod1 in enumerate(self.board):
        if not rod1: continue
        for j, rod2 in enumerate(self.board[i:]):
            if i == j: continue
            if not rod2 or rod2[-1] > rod1[-1]: moves.append((i, j))
    return moves
```
### `doMove(self, move)`
Do move produces a puzzle after the move was executed onto the puzzle.
```python
def doMove(self, move):
    newPuzzle = Hanoi(size=self.size)
    stacks = deepcopy(self.stacks)
    stacks[move[1]].append(stacks[move[0]].pop())
    newPuzzle.stacks = stacks
    return newPuzzle
```
