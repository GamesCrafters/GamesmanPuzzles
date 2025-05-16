# GamesmanPuzzles
[![Build Status](https://travis-ci.com/GamesCrafters/GamesmanPuzzles.svg?branch=master)](https://travis-ci.com/GamesCrafters/GamesmanPuzzles)
[![codecov](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles/branch/master/graph/badge.svg)](https://codecov.io/gh/GamesCrafters/GamesmanPuzzles)

A collection of Puzzles bundled together in a simple yet powerful Python interface. Developed as of part of the [UC Berkeley GamesCrafters.](http://gamescrafters.berkeley.edu/)

## Installation
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

Run from the base directory of the repository
```
cd puzzlesolver/players
python tui.py hanoi
```
to play a puzzle of Towers of Hanoi.

## Solving Puzzles
You can solve all the puzzles by running the following in the base project directory:
```
python -m scripts.solve
```

## Serving Puzzles

Run from the base directory of the respository
```
python -m scripts.server
```
to access the webserver locally. The server should be running at http://127.0.0.1:9001/.


### Routes
- `/health` : 
    - Returns the current health and status of the service.

      UWAPI health fields:
        - `status`: (String) `"degraded"` when CPU Usage & Virtual Memory Usage is => 90%, else `"ok"`. Indicates that GamesmanPuzzles is online.
        - `http_code`: (Integer) Always HTTP `200`. Indicates that GamesmanPuzzles is online.
        - `timestamp`: (Integer) ISO 8601 UTC timestamp of when the health response was made (e.g., `"2025-05-16T20:25:55Z"`).
        - `uptime`: (String) Time GamemsanPuzzles has been running in `Xd Yh Zm Ws` format.
        - `cpu_usage`: (String) The percentage of CPU currently used (e.g., `"21.2%"`).
        - `memory_usage`: (String) The percentage of total system memory currently used (e.g., `"10.1%"`).
        - `process_count`: (String) Number of processes currently running on the system.

      Below is an example response from `/health`:
      ```json
      {
        "cpu_usage": "92.2%",
        "http_code": 200,
        "memory_usage": "90.2%",
        "process_count": 875,
        "status": "degraded",
        "timestamp": "2025-05-16T23:46:50Z",
        "uptime": "4d 4h 0m 13s"
      }
    ```

- `/<puzzle_id>/<variant_id>/start/` 
  - Returns the initial position of the variant of ID `variant_id` of the puzzle of ID `puzzle_id`. If the puzzle supports randomized starting positions, the content of the response will correspond to a random initial position.

    The response contains two fields:
      - `position`: (String) The human-readable string representation of the position.
      - `autoguiPosition`: (String) The AutoGUI-formatted string corresponding to the position, which tells the frontend application how to render the position.

    Below is an example response for `/npuzzle/3/start/` which gives a starting position for the variant with `variant_id` "3" of the puzzle with `puzzle_id` "npuzzle" (i.e., the 8-Puzzle variant of the Sliding Number Puzzle).

    ```json
    {
        "position": "7-2453681",
        "autoguiPosition": "1_7-2453681"
    }
    ```

    Since the Sliding Number Puzzle supports randomized starting positions, this response is randomized. Below is another example response for `/npuzzle/3/start/`.

    ```json
    {
        "position": "62-581374",
        "autoguiPosition": "1_62-581374"
    }
    ```

- `/<puzzle_id>/<variant_id>/positions/?p=<position_string>`
  - Returns information about the position specified by `position_string` of the variant specified by `variant_id` of the game specified by `game_id`. This is used, for example, by GamesmanUni when it needs to load a new position every time a user makes a move.

    When using this route to get information about a position, `position_string` should be the human-readable string representation of the position, and NOT the AutoGUI-formatted position string corresponding to that position.

    The response contains the following fields:
      - `position`: (String) The human-readable string representation of the puzzle position.
      - `autoguiPosition`: (String) The AutoGUI-formatted string corresponding to the position, which tells the frontend application how to render the position.
      - `positionValue`: (String) The value of this position. This field will either be `win` (the puzzle is solvable from this position) or `lose` (the puzzle cannot be solved from this position).
      - `remoteness`: (Number, may be undefined) If `positionValue` is `win`, i.e., the puzzle is solvable from this position, then this is a non-negative integer indicating the number of moves needed to solve the puzzle from this position. If `positionValue` is `lose`, i.e., the puzzle cannot be solved from this position, then this field is undefined.
      - `moves`: (Array): A list of move objects, in no particular order. If there are no legal moves from this position, this is an empty array. Each move object contains the following fields:
        - `move`: (String) The human-readable string representation of the move.
        - `autoguiMove`: (String) An AutoGUI-formatted move string, which tells the frontend application how to render the button that the user can click to make this move.
        - `position`, `autoguiPosition`, `positionValue`, `remoteness` of the child position reached after making this move.
    
    Below is the response for position `-87125364` of the 8-Puzzle variant (`variant_id` of "3") of the Sliding Number Puzzle (`puzzle_id` of "npuzzle"), i.e., the response for `/npuzzle/3/positions/?p=-87125364`. The puzzle can be solved in as few as 28 moves and both legal moves make progress toward the solved state.

    ```json
    {
        "position": "-87125364", 
        "autoguiPosition": "1_-87125364",
        "positionValue": "win",
        "remoteness": 28,
        "moves": [
            {
                "autoguiMove": "M_1_0_x",
                "autoguiPosition": "1_8-7125364",
                "move": "8",
                "position": "8-7125364",
                "positionValue": "win",
                "remoteness": 27
            },
            {
                "autoguiMove": "M_3_0_x",
                "autoguiPosition": "1_187-25364",
                "move": "1",
                "position": "187-25364",
                "positionValue": "win",
                "remoteness": 27
            }
        ]
    }
    ```

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