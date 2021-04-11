# Contributing

## Setting up your workflow
Start by cloning this repository and switching to the dev branch.
```bash
git clone https://github.com/GamesCrafters/GamesmanPuzzles
cd GamesmanPuzzles
```
Load the dependencies and set up the environment. It's recommended to use a [virtualenv](https://docs.python.org/3/library/venv.html) for this step. Make sure to be using Python3 instead of Python2.
```bash
pip install -r requirements.txt
pip install -e
```
## Contributing a Change (Adding a Puzzle or Solver)
Guidelines for contributing puzzles or solvers
1. To contribute a Puzzle, follow the guidelines provided in the [tutorials](/guides/tutorial). Add your dependencies to the `puzzlelist` located in the [`__init__.py`](/puzzlesolver/puzzles/__init__.py) file. 
2. To contribute a Solver, inherit from the base Solver class and place your solver source file in the [solvers directory](/puzzlesolver/solvers).
3. Every solved Puzzle must have their respective test. The bare minimum for a test is to check the remoteness of an arbitrary position that is not a SOLVABLE position.

## Pull Requests

Every change must be done using a pull request. Here are the directions [to fork a repository and make a change.](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) 

The best way to start a pull request is to create a new branch. 
```bash
git pull # Update all branches
git checkout -b <your-branch-name>
```
The conventional branch naming system is `<your_name>/<feature_name>`.

After you make your changes, commit and push. As a nonspoken rule, **COMMIT WELL, PUSH OFTEN**. Making good commit messages allows others to understand your work, as well as pushing your changes allow others to see your work and comment on potential fixes.
```bash
git commit -m "Your commit message here"
git push
```

## Testing
You can run the local tests simply by the command. All tests must pass before submission.
```
pytest
```

Continuous integration has also been set up for every change you push. You can view the latest build [here.](https://travis-ci.com/github/GamesCrafters/GamesmanPuzzles/branches)