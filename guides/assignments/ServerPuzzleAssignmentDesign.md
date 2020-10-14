# Server Puzzle Assignment (Design part) (Due 10/21)
Alright, now it's time to take the training wheels off and develop your own ServerPuzzle. Your assignment is to design and develop a ServerPuzzle based on the tutorials and format set up in GamesmanPuzzles.

Before developing the ServerPuzzle, you must visualize how your Puzzle would work. What should be the default variant? How many positions must be hashed? How will the puzzle progress? 

This design process will be represented with a writeup. You must submit the writeup in PDF form. Include these in your writeup:

- Your name/Team names
- Puzzle
    - Puzzle Name
    - Puzzle ID
        - Simple identifier of a Puzzle. (Example: 'hanoi') 
    - Puzzle Visualization
        - A picture of the Puzzle.
        - Must match default Variant
    - Short Description of Puzzle 
        - About 1-2 paragraphs
        - Should contain how to play and win.
        - State why you think it's a good addition to GamesmanPuzzles
- Position
    - Position representation (Check Example A below)
- Moves
    - The type of Legal moves in the Puzzle 
        - Forward, Bidirectional, or Both
    - Move representation (Check Example A below)
        - Moves should be represented as a tuple with two entries. 
        - You should represent complex entries as single numbers or letters.
- Variants (Must have at least two Variants, including the default Variant)
    - Variant Name
    - Number of possible positions
        - Also include calculation
    - A Default Variant should have a small minimum remoteness (5-20 moves) and be easy to solve (10000 positions at max). You wouldn't have any problems solving it multiple times.
- (Optional) Optimization
    - Example topic: Reduced number of positions with Hash tricks

Submit your writeup in the shared Google Drive folder by the listed time (10/21/20). The Google Drive link will be posted on Slack. 

## Examples
### Example-A:
The Tower of Hanoi board can be represented in this String representation:
```
[[3, 2, 1], [], []]
```
A move can be represented as a tuple with Whole Numbers. For example, a move from the first rod to the second rod can be represented as:
```
(0, 1)
```
Another example is chess. A white knight move can be represented as
```py
("b1", "c3")
```
