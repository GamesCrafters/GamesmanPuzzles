# Server Introduction
GamesmanPuzzles provides a Web API to display values of puzzles. This guide will adapt our puzzle from the previous steps into a format which can be displayed onto the Web API.

You can manually run the server by running
```python
python -m puzzlesolver.server
```
and accessing [http://localhost:9001](http://localhost:9001). You can explore the Web API using the documentation (to do soon).

## Prerequisites

After this guide, you should able to display a puzzle in a test application.

Begin by importing all the extra dependencies in our Hanoi puzzle that we made before
```python
from puzzlesolver.puzzles import ServerPuzzle
```

Change the class we inherit from Puzzle to ServerPuzzle

```python
class Hanoi(ServerPuzzle):
```

The next steps would be implementing extra functions:
[Next Step: PuzzleID](08_PuzzleID.md)
