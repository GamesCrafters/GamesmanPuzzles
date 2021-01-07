# Position Introduction

```
GET puzzles/<puzzle_id>/<variant_id>/<position_id>
```
Positions strings allow users to query into our PuzzleSolver and find the remoteness of positions. Thus, it's the most crucial functionality and contains most complex methods to implement for a ServerPuzzle. This part of the guide will be implementing those methods.

## Serialization
When users are accessing the Web API, they need a way to input a puzzle position and return a result. We can do this by **serializing** the puzzle into a string code, which can be **deserialized** back into a puzzle.

#### **`toString(**kwargs)`**

Serializing is to take an object and convert it into string form. The string returned must be unique enough to turn back to said object. *Note: this is different from a hash, as a hash can be the same for two puzzles if one is simply a variation of the other.*

To encapsulate this serialization behavior, let's redefine `toString`. We cannot use the simple `str(self.stacks)` representation as before since the resulting string has non URL-friendly characters, so we're modifying the implementation to use dashes and underscores.
```python
def toString(self, **kwargs):
    result = []
    for stack in self.stacks:
        result.append("_".join(str(x) for x in stack))
    return "-".join(result)
```

#### **`fromString(cls, positionid, **kwargs)`**

Deserializing is to take a string and encode it back into an object. After serializing an puzzle, deserializing the serialization must return the same puzzle. To be consistent with our naming convention, the function's name will be `fromString`. 

**Note: It is very important to raise TypeErrors and ValueErrors** in this function. Like `doMove`, this is another way users can manipulate puzzle state, but this time it's much more harder to control. For example, this implementation of Hanoi has the following requirements:
- No disk is ontop of a smaller disk
- No duplicate disks
- All disks have to be ints
- Only supports 3 stacks (not true in the official implementation)

```python
@classmethod
def fromString(cls, positionid, **kwargs):
    # Checking if the positionid is a str
    if not isinstance(positionid, str):
        raise TypeError("PositionID is not type str")
    
    # Checking if the string can be split into 3 stacks
    stacks = positionid.split("-")
    if not stacks or len(stacks) != 3:
        raise ValueError("PositionID cannot be translated into Puzzle")
    
    puzzle = Hanoi()
    seen = set()
    
    try:        
        for string in stacks:
            if string != "":
                # Check that all disks are ints
                stack = [int(x) for x in string.split("_")]
                # Check for duplicate disks
                if seen.intersect(stack): raise ValueError
                seen = seen.union(stack)                
                puzzle.stacks.append(stack)
            else: puzzle.stacks.append([])        
    except ValueError:
        raise ValueError("PositionID cannot be translated into Puzzle")
 
    return puzzle   
```

## Start Position
#### **`generateStartPosition()`**

This function is mainly here to give a starting and example position for a variant in a puzzle, and will be on display at `/puzzles/<puzzle_id>/<variant_id>/`.
```python
@classmethod
def generateStartPosition(cls, variantid, **kwargs):
    if not isinstance(variantid, str): raise TypeError("Invalid variantid")
    if variantid not in Hanoi.variants: raise ValueError("Out of bounds variantid")
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
