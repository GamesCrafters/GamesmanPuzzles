# Moves
#### `generateMoves(self, movetype="all", **kwargs)`
This function allows the puzzle to generate possible moves and move the puzzle forward. It should return all possible moves (including undos) that any player can make on the puzzle. For Hanoi, a move is to move the top piece of any rod onto another rod as long as it satisfies the restriction that a bigger ring cannot be on top of a smaller ring.

**Note:** We also have to include "undo" moves, which are moves that may not technically be legal (i.e. undoing a move in Chess could be uncapturing a piece or a pawn moving backwards). We need these moves as our GeneralSolver moves from the end state to the start states. Consider if undoing any move is a legal move in your puzzle and if it isn't, implement `generateLegalMoves(self)` as well, which returns a list of legal moves.  
```python
def generateMoves(self, movetype="all", **kwargs):
    moves = []
    for i, stack1 in enumerate(self.stacks):
        if not stack1: continue
        for j, stack2 in enumerate(self.stacks):
            if i == j: continue
            if not stack2 or stack2[-1] > stack1[-1]: moves.append((i, j))
    return moves
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
