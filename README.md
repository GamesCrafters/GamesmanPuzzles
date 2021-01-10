# GamesmanPuzzles
[![Build Status](https://travis-ci.com/GamesCrafters/GamesmanPuzzles.svg?branch=master)](https://travis-ci.com/GamesCrafters/GamesmanPuzzles)
[![codecov](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles/branch/master/graph/badge.svg)](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles)

A Python Package dedicated to Puzzle solving. Developed as of part of the [UC Berkeley GamesCrafters.](http://gamescrafters.berkeley.edu/)
## Building from source
Clone this repository and install the dependencies (it's recommended to use a virtualenv when installing dependencies of any project):
```
git clone https://github.com/GamesCrafters/GamesmanPuzzles.git
cd GamesmanPuzzles
pip install -r requirements.txt
pip install -e .
```

Run from the base directory of the repositiory
```
python puzzleplayer.py hanoi
```
to play a puzzle of Towers of Hanoi

Run from the base directory of the respository
```
python server.py
```
to access the webserver. The server should be running at http://127.0.0.1:9001/.

## Exploring GamesmanPuzzles
Tips for exploring this repository:
1. [Follow the guides and learn how to create a puzzle and a solver!](guides)
2. Definitely explore the [puzzlesolver](puzzlesolver) in depth.
3. Understand what a [puzzle tree](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree) is. 

## Contributing to GamesmanPuzzles
Guidelines for contributing puzzles or solvers
1. Puzzles/solvers must be pushed into their respective directory encompassed in the `puzzlesolver` directory.
2. Every solved Puzzle must have their respective test. The bare minimum for a test is to check the remoteness of an arbitrary position that is not a SOLVABLE position.

Every change must be done using a pull request. Here are the directions [to fork a repository and make a change.](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) 
