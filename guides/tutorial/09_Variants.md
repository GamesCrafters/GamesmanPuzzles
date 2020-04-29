# Variants Introduction

```
GET puzzles/<puzzle_id>/<variant_id> 
```

Sometimes we want our puzzle to support multiple versions of itself. For example, in Hanoi we can support puzzles with more than just three discs. To support this, we introduce **Variants**.

## Variants
A **variant** is a modified version of a puzzle (i.e. more pieces, different orientation). Each puzzle variant is independent of each other, defined to be that there is no position in one variant that can exist in another variant.

Each initialized puzzle will have a different variant, so we need to modify the `__init__()` and `generateSolutions()` functions to support different variant (size) numbers.

**`__init__()`**
```python
def __init__(self, size=3, **kwargs):
    self.stacks = [
        list(range(size, 0, -1)),
        [],
        []
    ]
```

**`generateSolutions()`**
```python
def generateSolutions(self, **kwargs):
    newPuzzle = Hanoi(size=int(self.variant))
    newPuzzle.stacks = [
        [],
        [],
        list(range(int(self.variant), 0, -1))
    ]
    return [newPuzzle]
```

We also need a property to get the current variant of the puzzle. (`@property` is a tag that we use to defined the function as a property of the function, such as `Hanoi().variant`)
```python
@property
def variant(self):
    size = 0
    for stack in self.stacks:
        size += len(stack)
    return str(size)
```
Our server requires that we define a dictionary with variant ids as the keys as well as different Solver classes as the values. *Note: The reason for this is that different variants may use different solvers.*

Just for these purposes, lets consider only variants up to 3 as well as using the GeneralSolver as the main solver.
```python
variants = {
    str(i) : GeneralSolver for i in range(1, 4)
}
```
[Next Step: Positions](10_Positions.md)