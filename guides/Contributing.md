# Contributing
## About
This repository has <s>two</s> one main branches.
- `master`, which is the main branch used to regulate releases and contains the most up to date release.
- <s>`dev`, which is the main branch for development, experimental, and testing purposes. It will usually contain the next release.</s>

<s>Contributors to this repository should clone and be up to date with the `dev` branch, while using `master` as reference. </s>
## Setting up your workflow
Start by cloning this repository and switching to the dev branch.
```bash
git clone https://github.com/GamesCrafters/GamesmanPuzzles
cd GamesmanPuzzles
git checkout dev
```
Load the dependencies. It's recommended to use a [virtualenv](https://docs.python.org/3/library/venv.html) for this step. Make sure to be using Python3 instead of Python2.
```bash
pip install -r requirements.txt
```
## Contributing a Change
Refer to [Where to Put My Stuff](wheretoputmystuff.md) for guidance when contributing.

Whenever you want to make a change to any of the main branches, you must use pull requests. Push access to these branches is restricted to only administrators. 

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
When you feel like the branch is ready to be pushed into a main branch, make a pull request. [Here are directions in doing so](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
