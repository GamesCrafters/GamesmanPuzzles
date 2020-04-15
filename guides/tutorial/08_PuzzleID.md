# Puzzle ID
```
GET puzzles/<puzzle_id>
```
The first part of our url is the identification of our puzzle. This is a class variable and can be used to access the variants (next section). 

Define it inside your class:
```python
class Hanoi(ServerPuzzle):
    puzzleid = 'hanoi'
```

[Next Step: Variants](09_Variants.md)