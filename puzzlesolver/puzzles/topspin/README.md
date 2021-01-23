Yishu Chao

Puzzle Name: Top Spin

Puzzle ID: “top_spin”

Puzzle Visualization:
<p align="center">
    <img src=TopSpin.PNG>
</p>

Short Description of Puzzle:
The standard Top Spin puzzle comes with 20 beads on an oval track. Players can move the beads forward or backward by simply pushing on them, and all the beads will advance as a single unit. In the middle of the top straight edge, there is a spinner that takes in four and only four beads and reverses their order. When all the beads are in sorted order, the game is over (note that since the track is circular, there is no defined start). This puzzle might seem simple; however, since the only way to change the ordering of the beads is through the top spinner, it could get tricky once the player has only four or less than four beads out of place. Many reviews online have mentioned that this puzzle is somewhat reminiscent of a Rubik’s cube, but of course 2-Dimensional and simpler. Since this is a game that concerns permutations of the beads, I am interested in seeing given a starting order, what is the minimum number of steps it takes to solve the puzzle.
 
Position representation:
In order to keep the total number of positions under 10,000, I will implement a smaller version of the default variant -- one with 8 beads.

Position can be represented with a string representation shown below:

\[ 1 , 2 , \[3 , 4 , 5 , 6\] , 7 , 8\]  

where the middle list represents beads are that in the spinner and can be reversed.

Legal moves:
All legal moves are bidirectional since the player can push beads in either direction along the track. After that pushing the beads, the spinner will reverse the beads in it at the end of every move. 

Since all the beads are placed on an oval track, if the players were to push all the beads 1 place forward, 1 would wrap around to the end of the list. 

Move representation:
Moves will be represented with a tupule, like this:

move = (n), n<=7

move is the number of positions the player wants to advance and could be either positive or negative, depending on how much the player wants to push the beads forward/backward.  

Variants
Variant Name: 8-bead (default) 

Number of possible positions:
A list with N numbers should have N! permutations; however, since the puzzle is played on a circular track, start does not matter, so some of the strings are essentially the same, and after removing symmetry, there should be (N-1)! Permutations. Which four beads are in the spinner should not matter since those are also included in our permutation calculations. In this case, 5040 positions. 

Minimum remoteness should depend on the starting track.

Variant Name: 7-bead

Number of possible positions:
Similar to the analysis above for the default variant, it should have 6! = 720 positions. 
I think it would also be interesting to look at how reducing/increasing the size spinner (i.e. how many beads can be reversed) could affect game play. 


