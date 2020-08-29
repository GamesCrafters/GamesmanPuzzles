# Assignment: Develop your own ServerPuzzle
Alright, now it's time to take the training wheels off and develop your own ServerPuzzle. Your assignment is to design and develop a ServerPuzzle based on the tutorials and format set up in GamesmanPuzzles.

### Table of Contents
- [Design](#design)
- [Develop](#develop)
- [Examples](#examples)

## Design
Before developing the ServerPuzzle, you must visualize how your Puzzle would work. What should be the default variant? How many positions must be hashed? How will the puzzle progress? 

This design process will be represented with a writeup. You must submit the writeup in PDF form. Include these in your writeup:

- Your name/Team names
- Puzzle
    - Puzzle Name
    - Puzzle ID
        - Simple identifier of a Puzzle. (Example: 'hanoi') 
    - Puzzle Visualization
        - A picture of the Puzzle.
        - Must match default Variant
    - Short Description of Puzzle 
        - About 1-2 paragraphs
        - Should contain how to play and win.
- Position
    - Position representation ([example](###Example-A))
- Moves
    - The type of Legal moves in the Puzzle 
        - Forward, Bidirectional, or Both
    - Move representation ([example](###Example-A))
        - Moves should be represented as a tuple with two entries. 
        - You should represent complex entries as single numbers or letters.
- Variants (Must have at least two Variants, including the default Variant)
    - Variant Name
    - Number of possible positions
        - Also include calculation
    - A Default Variant should have a small minimum remoteness (5-20 moves) and be easy to solve (20000 positions at max). You wouldn't have any problems solving it multiple times.
- (Optional) Optimization
    - Example topic: Reduced number of positions with Hash tricks

Submit your writeup at Gradescope by the listed time. 

## Develop
Similar to how you implemented Hanoi, implement your ServePuzzle and follow the [tutorial steps](../tutorial). You may refer to the already existing puzzles ([Hanoi](../../puzzlesolver/puzzles/hanoi.py)) for guidance.

### Testing
You are also responsible for implementing test sets following the format, located in `GamesmanPuzzles/tests/puzzles/test_<your_puzzle_name here>`. 

- `testHash()`
    - Tests the expected behavior of the hash function on the puzzle states. 
- `testSerialization()`
    - Tests if serialization and deserialization works both ways.
- `testPrimitive()`
    - Tests if the start state and end state outputted the right primitives.
- `testMoves()`
    - Tests a specific scenario and checks if the moves inputted resulted in the expected state, generated moves, and expected invalid moves.
- `testPositions()`
    - Tests the default start state and finish positions matches the expected serializations.
- `testValidation()`
    - Tests four invalid serializations and checks if it raises an error.
- `testServerPuzzle()`
    - Tests server functionality by trying out a series of inputs.

 You are EXPECTED to take much inspiration from the [example test suite of Hanoi](../../tests/puzzles/test_Hanoi.py). 
 
 To run your tests, execute in the GamesmanPuzzles directory:
```
pytest --cov puzzlesolver
```
Submit this project by creating a pull request to the Master branch. Refer to [Contributing](../Contributing.md) for more info.

### Additional Steps and Tips To Consider
- A real ServerPuzzle should not be using GeneralSolver as its main solver, as each request for the remoteness of a position for our server would have the GeneralSolver solve the puzzle. Consider using one of our persistence solvers like SqliteSolver or IndexSolver. The hash used in the tutorial should NOT be used for IndexSolver.
- Files should be placed properly in their respected directories. Refer to [Where To Put My Stuff](../wheretoputmystuff.md) for more info. You should also adjust your dependencies based on the location of the file.

## Examples
### Example-A:
The Tower of Hanoi board can be represented in this String representation:
```
[[3, 2, 1], [], []]
```
A move can be represented as a tuple with Whole Numbers. For example, a move from the first rod to the second rod can be represented as:
```
(0, 1)
```
Another example is chess. A white knight move can be represented as
```py
("b1", "c3")
```
