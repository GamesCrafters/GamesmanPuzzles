# Moves
Let's review how moves work in the puzzle tree. Below is a graph with the numbered nodes as Puzzles and the directed edges as Moves.

<p align="center">
<img src='graph.png' width=200>
</p>

### Move types
We'll define five types of moves for each node:
- **Forward**: All moves from a Puzzle P to another Puzzle Q if there exists a Legal move from P to Q, **but** there doesn't exist a Legal move from Q to P.  
    - Examples: (1,2), (3,1)
- **Bidirectional**: All moves from a Puzzle P to another Puzzle Q if there exists a Legal move from P to Q **and** there exists a Legal move from Q to P.
    - Examples: (1,4), (4,1)
- **Backward**: All moves from a Puzzle P to another Puzzle Q if there **doesn't** exist a Legal move from P to Q **but** there exists a Legal move from Q to P.
    - Examples: (1,3), (2,1)
- **Legal:** Any move possible from the current Puzzle based on the Puzzle rules (i.e capturing and moving pawns forward in Chess). Also equivalent to the combination of Forward and Bidirectional moves
- **Undo:** Equivalent to the combination of Bidirectional and Backward moves.

The GeneralSolver makes good use of Undo moves when solving position values and calculating remoteness (more on that in the Solver guide). Hanoi only has Bidirectional moves, so there isn't a need to generate Forward or Backward moves, however, when considering other Puzzles such as Peg solitare (which jumps over and captures adjacent pieces), make sure that `generateMoves` returns moves for every `movetype`.

### Implementation

#### `generateMoves(self, movetype="all", **kwargs)`
This function allows the puzzle to generate possible moves and move the puzzle forward. It should return all possible moves based on the `movetype` variable. Hanoi only has bidirectional moves, so if we're inputted a `movetype` of `'for'` or `'back'`, we should return no moves. Possible values of `movetype` are `['for', 'back', 'bi', 'undo', 'legal', 'all']`.

```python
def generateMoves(self, movetype="all", **kwargs):
    if movetype=='for' or movetype=='back': return []
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