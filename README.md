# GamesmanPuzzles
[![Build Status](https://travis-ci.com/GamesCrafters/GamesmanPuzzles.svg?branch=master)](https://travis-ci.com/GamesCrafters/GamesmanPuzzles)
[![codecov](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles/branch/master/graph/badge.svg)](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles)

A collection of Puzzles bundled together in a simple yet powerful Python interface. Developed as of part of the [UC Berkeley GamesCrafters.](http://gamescrafters.berkeley.edu/)

## Installation
Install via pip (tested on MacOS and Linux):
```
pip install GamesmanPuzzles
```
For more info about the package, check out this little [guide](guides/build.md).
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
cd puzzlesolver/players
python tui.py hanoi
```
to play a puzzle of Towers of Hanoi

Run from the base directory of the respository
```
python server.py
```
to access the webserver. The server should be running at http://127.0.0.1:9001/.

## Testing
To run all the tests, run the following command:
```
pytest --cov puzzlesolver
```

## Exploring GamesmanPuzzles
Tips for exploring this repository:
1. [Follow the guides and learn how to create a puzzle and a solver!](guides)
2. Definitely explore the [puzzlesolver](puzzlesolver) in depth.
3. Understand what a [puzzle tree](https://nyc.cs.berkeley.edu/wiki/Puzzle_tree) is. 

## Contributing to GamesmanPuzzles
See [contributing](/guides/Contributing.md)
### Contributors:
Fall 2020:

[Anthony Ling](https://github.com/Ant1ng2), [Mark Presten](https://github.com/mpresten), [Arturo Olvera](https://github.com/olveraarturo)

Spring 2021:

Anthony Ling, Mark Presten, [Brian Delaney](https://github.com/briancdelaney), [Yishu Chao](https://github.com/yishuchao), [Sophia Xiao](https://github.com/sofa-x)
