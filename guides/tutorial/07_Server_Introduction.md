# Server Introduction
GamesmanPuzzles provides a Web API to display values of puzzles. This guide will adapt our puzzle from the previous steps into a format which can be displayed onto the Web API.

You can manually run the server by running **only after all the puzzles have been solved and stored in binary files. This probably hasn't been done in your local system yet, but it is not necessary for this tutorial.**
```python
python server
```
and accessing [http://localhost:9001](http://localhost:9001).

## About the Server

The GamesmanPuzzles server is an HTTP server that serves Puzzle data in a JSON format. You may find it similar to GamesCraftersUWAPI, the web server that serves Game data.

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
