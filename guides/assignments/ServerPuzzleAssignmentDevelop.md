# Server Puzzle Assignment (Develop part) (Due 11/4/20)
Now that you have a general idea of what kind of Puzzle you want to implement, it is time to develop!. Similar to how you implemented Hanoi, implement your ServerPuzzle and follow the [tutorial steps](../tutorial). You may refer to the already existing puzzles ([Hanoi](../../puzzlesolver/puzzles/hanoi.py)) for guidance.

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
