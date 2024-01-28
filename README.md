# GamesmanPuzzles
[![Build Status](https://travis-ci.com/GamesCrafters/GamesmanPuzzles.svg?branch=master)](https://travis-ci.com/GamesCrafters/GamesmanPuzzles)
[![codecov](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles/branch/master/graph/badge.svg)](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles)

A collection of Puzzles bundled together in a simple yet powerful Python interface. Developed as of part of the [UC Berkeley GamesCrafters.](http://gamescrafters.berkeley.edu/)

## Installation
### Building from source
Clone this repository and install the dependencies (it's recommended to use a virtualenv when installing dependencies of any project):
```
git clone https://github.com/GamesCrafters/GamesmanPuzzles.git
cd GamesmanPuzzles
pip install -r requirements.txt
pip install -e .
```

To get optional closed-form solver for Lights Out, run the following commands from the project's root directory:
```
cd puzzlesolver/extern
python setup.py build_ext --inplace
```

Run from the base directory of the repositiory
```
cd puzzlesolver/players
python tui.py hanoi
```
to play a puzzle of Towers of Hanoi

### Web app
The Web application requires two things:
1. Desired Puzzles to be solved
2. Server to be running

#### Solving Puzzles
You can solve all the puzzles by running the following in the base project directory:
```
python -m scripts.solve
```

#### Serving Puzzles

Run from the base directory of the respository
```
python -m scripts.server
```
to access the webserver locally. The server should be running at http://127.0.0.1:9001/.


##### Routes

`http://localhost:9001/<puzzle_id>/<variant_id>/start/` gives the initial position of the variant of ID `variant_id` of the puzzle of ID `puzzle_id`. If the puzzle supports randomized starting positions, the content of the response will correspond to a random initial position.
- Example: http://localhost:9001/npuzzle/3/start/ will give a starting position of the variant with ID “3” of the puzzle with ID “npuzzle”, i.e., variant 3 of the sliding number puzzle.

`http://localhost:9001/<puzzle_id>/<variant_id>/positions/<human_readable_position_string>/` shows information about the puzzle position represented by `human_readable_position_string` of the variant of ID `variant_id` of the puzzle of ID `position_id`.
- Example: http://localhost:9001/npuzzle/3/positions/4325718-6/ will show the position information for position represented by the string 4325718-6 of variant 3 of the sliding number puzzle.

## Testing (Broken)
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
Spring 2020: [Anthony Ling](https://github.com/Ant1ng2), [Mark Presten](https://github.com/mpresten), [Arturo Olvera](https://github.com/olveraarturo)

Fall 2020: Anthony Ling, Mark Presten, [Brian Delaney](https://github.com/briancdelaney), [Yishu Chao](https://github.com/yishuchao), [Sophia Xiao](https://github.com/sofa-x)

Spring 2021: Anthony Ling, Mark Presten, [Mia Campdera-Pulido](https://github.com/miacampdera)

Fall 2022: [Linh Tran](https://github.com/Linh-Tran-nlt)

Spring 2023: [Christopher Nammour](https://github.com/chrisnammour)

Current: [Cameron Cheung](https://github.com/cameroncheung00), [Robert Shi](https://github.com/robertyishi)