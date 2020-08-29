# Position Introduction

```
GET puzzles/<puzzle_id>/<variant_id>/<position_id>
```
Positions strings allow users to query into our PuzzleSolver and find the remoteness of positions. Thus, it's the most crucial functionality and contains most complex methods to implement for a ServerPuzzle. This part of the guide will be implementing those methods.

## Serialization
When users are accessing the Web API, they need a way to input a puzzle position and return a result. We can do this by **serializing** the puzzle into a string code, which can be **deserialized** back into a puzzle.

#### **`serialize()`**

Serializing is to take an object and convert it into string form. The string returned must be unique enough to turn back to said object. *Note: this is different from a hash, as a hash can be the same for two puzzles if one is simply a variation of the other.*
```python
def serialize(self, **kwargs):
    result = []
    for stack in self.stacks:
        result.append("_".join(str(x) for x in stack))
    return "-".join(result)
```

#### **`deserialize()`**

Deserializing is to take a string and encode it back into an object. After serializing an puzzle, deserializing the serialization must return the same puzzle.

**Note:** Deserializing should raise a `PuzzleException` (found in the `puzzlesolver.util` module) if it encounters invalid puzzleid input.

```python
@classmethod
def deserialize(cls, positionid, **kwargs):
    puzzle = Hanoi()
    puzzle.stacks = []
    stacks = positionid.split("-")
    for string in stacks:
        if string != "":
            stack = [int(x) for x in string.split("_")]
            puzzle.stacks.append(stack)
        else: puzzle.stacks.append([])
    return puzzle
```

## Validation

When the user interacts with the server, occasionally the user may input positionids that are not valid. We want to make sure the user inputs proper strings, and return helpful messages when they don't. Thus, we must be ablle to validate user input. Validation is built-in as default behavior for every ServerPuzzle and can be observed in the `validate` function. It relies on the implementation of `deserialize` and a new function `isLegalPosition`.

#### **`isLegalPosition()`**

`isLegalPosition()` is a classmethod that checks if a given string is a valid Puzzle object as well as follows the rules of the given puzzle. For example, you cannot stack a larger disc ontop of a smaller disc in Towers of Hanoi.
```python
@classmethod
def isLegalPosition(cls, positionid, variantid=None, **kwargs):
    try: puzzle = cls.deserialize(positionid)
    except: return False
    unique = set()
    if len(puzzle.stacks) != 3: return False
    for stack in puzzle.stacks:
        if stack != sorted(stack, reverse=True):
            return False
        unique.update(stack)
    if len(unique) != int(puzzle.variant) or min(unique) != 1 or max(unique) != int(puzzle.variant):
        return False
    return True
```

## Start Position
#### **`generateStartPosition()`**

This function is mainly here to give a starting and example position for a variant in a puzzle, and will be on display at `/puzzles/<puzzle_id>/<variant_id>/`.
```python
@classmethod
def generateStartPosition(cls, variantid, **kwargs):
    if not isinstance(variantid, str): raise TypeError("Invalid variantid")
    if variantid not in Hanoi.variants: raise IndexError("Out of bounds variantid")
    return Hanoi(size=int(variantid))
```

## Conclusion:
To test if the ServerPuzzle has been implemented, add the following on the end of your file:
```python
from puzzlesolver.server import test_puzzle
test_puzzle(Hanoi)
```
Then run:
```bash
python <your_python_file_name>.py
```
Go to the link the app is running on and test out all the paths (i.e. `hanoi/3/3_2_1--`). If the remoteness of the position is 7 and the remoteness of all other positions is 7 or 6, then congrats! You have successfully implemented a Server Puzzle! 
