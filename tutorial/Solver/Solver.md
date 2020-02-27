# The Solver Function

Our GeneralSolver uses a bottom to top BFS algorithm to classify positions of the puzzle. This guide assumes that you have checked out the following documentation for a [puzzle tree.](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree)

### Introduction
The solve function is the core of all solvers in the GamesmanPuzzles and is used to classify positions of the puzzle. For this solver, we will use memoization and tree traversal.

### 1. Memory search 
In the case when our position already exists in memory or have already calculated this position, we just lookup the value using the hash of the puzzle.

```python
def solve(self, puzzle):
    if hash(puzzle) in self.values: return self.values
```

### 2. Breadth algorithm
Remember back in the puzzle project, we defined a few important functions that were meant to be used for this solver. These functions are:
- ```generateSolutions(self):``` Generates all the positions that have a primitive value of SOLVABLE.
- ```generateMoves(self):``` Generates all moves from that position (including undos).
- ```doMove(self, move):``` Returns a new Puzzle object with ```move``` executed. 

Following the steps of the algorithm we defined in [puzzle tree:](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree)

1. Find all the winstates of a Puzzle and set their remoteness to be 0.
2. Generate all positions that have a move towards the initial position in step 1.
3. Set all of our generated positions to have a remoteness equal to the initial position plus 1.
4. Repeat steps 2 and 3 for all new generated positions.

Splitting the algorithm into two separate parts:

Step 1: (the ```helper``` function would be defined in Step 2, 3, & 4)
```python
ends = puzzle.generateSolutions()
for end in ends: 
    self.values[hash(end)] = PuzzleValue.SOLVABLE
    self.remoteness[hash(end)] = 0
    helper(self, end)
if hash(puzzle) not in self.values: self.values[hash(puzzle)] = PuzzleValue.UNSOLVABLE
return self.values[hash(puzzle)]

```

Step 2, 3, & 4: 
```python
def helper(self, puzzle):
    queue = q.Queue()
    queue.put(puzzle)
    while not queue.empty():
        puzzle = queue.get()
        for move in puzzle.generateMoves():
            nextPuzzle = puzzle.doMove(move)
            if hash(nextPuzzle) not in self.remoteness:
                self.values[hash(nextPuzzle)] = PuzzleValue.SOLVABLE
                self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                queue.put(nextPuzzle)
```

The final solve function should look like this:
```python
def solve(self, puzzle):
    if hash(puzzle) in self.values: return self.values[hash(puzzle)]        
    def helper(self, puzzle):
        queue = q.Queue()
        queue.put(puzzle)
        while not queue.empty():
            puzzle = queue.get()
            for move in puzzle.generateMoves():
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in self.remoteness:
                    self.values[hash(nextPuzzle)] = PuzzleValue.SOLVABLE
                    self.remoteness[hash(nextPuzzle)] = self.remoteness[hash(puzzle)] + 1
                    queue.put(nextPuzzle)

    ends = puzzle.generateSolutions()
    for end in ends: 
        self.values[hash(end)] = PuzzleValue.SOLVABLE
        self.remoteness[hash(end)] = 0
        helper(self, end)
    if hash(puzzle) not in self.values: self.values[hash(puzzle)] = PuzzleValue.UNSOLVABLE
    return self.values[hash(puzzle)]
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
If you have a Solver value of SOLVABLE, congrats! You have successfully implemented a Solver!

## Extras
Ponder on these questions in how we can optimize this solver
- Try thinking of a way to parallelize this solver.
- Are there any ways we can solve this not through BFS?
