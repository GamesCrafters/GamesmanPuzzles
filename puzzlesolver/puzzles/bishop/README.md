# Bishops
- Made by: Brian Delaney
- Fall Semester 2020
- Puzzle ID: bishop

## Visualization:
<p align="center">
    <img src=Bishops.PNG>
</p>

## Description:
The Bishop’s Puzzle is a puzzle that I remember solving from a video game called “The 7th Guest”. It is played on a small chessboard, with 5 rows and 4 columns in the original. In this puzzle’s original form, the puzzle begins with 4 white bishops placed on the 4 squares on the board’s bottom row, and 4 black bishops placed on the 4 squares on the board’s top row. (The white-squared and black-squared bishops are symmetric; for simplicity, I will only program one of these.) The goal of the puzzle was to move the bishops so that the black bishops were in the white bishops’ starting positions, and vice versa. This is done via a series of normal bishop moves: a bishop can move diagonally any number of spaces. There is no restriction that white and black moves must alternate. However, no bishop can be moved to a position where it can be captured by a bishop of the opposite color. For example, from the starting position above, the move a1 -> d4 is illegal, because then the white bishop we moved could be captured by the black bishop at c5. I remember this puzzle being deceptively complicated for its size, which is why I think studying it further is worthwhile.

## Position:
The game’s position can be represented by two lists of tuples: one representing the locations of the white bishops, and one representing the locations of the black bishops. Each tuple will consist of an x- and y- coordinate: the piece’s location. (These can be easily translated to and from normal chess location notation: e.g. (0, 0) could be a1). Beyond this, we will need to store the dimensions of the board, because this cannot be calculated from the location of each bishop. This can be collapsed into a string notation via something like “5_4_a1-a3_e1-e3”  to represent the starting position.

## Move:
A move can be a tuple of two entries: the starting square and the ending square. An example legal move from the starting position would be (“a1”, “b2”). The nature of this puzzle makes all moves bidirectional. Bishop moves are bidirectional in normal chess, no pieces are captured, and both the start and end location of a move must not be threatened by the opposing color (if the former was, the opposite colored bishop cannot have moved into the threatening position).

## Variants:
The default variant is the one that appeared in “The 7th Guest:” the 5x4 variant. We can just call it “5x4”. It’s not trivial to calculate the number of valid positions because the cannot-enter-a-threatened-position rule is difficult to express mathematically, but we can apply a reasonable upper bound. The 5x4 chessboard has 10 spaces of each color (we only use one of the colors). The 2 white bishops can only be placed in \binom(10, 2) = 45 ways. These bishops constrain the location of the black bishops. The minimum number of the remaining 8 spaces that are constrained this way is 4 (place the white bishops at a1 and b2, for instance), which means there are 4 remaining spaces for the black bishops. These can be placed in \binom(4,2)=6 ways, so an upper bound on the total number of positions is 45*6=270. (I solved the puzzle again for this writeup: the starting position has remoteness 18).  
The two variants I plan to implement are the 7x4 and 7x6 variant (the latter will have 3 bishops instead of 2). The 7x4 variant has a number of positions upper-bounded at \binom(14,2) * \binom(8,2)=91*28=2548 positions.  The 7x6 variant has a number of positions upper-bounded at \binom(21,3) * \binom(10,3) (at minimum, 8 spaces can be prohibited, at least by a cursory judgement) =1330*120=159,600 positions. (It’s easy to see why I’m hesitant to solve a 4-bishop problem.)

## Optimization:
A similar hash trick to the one Prof. Garcia used with tic-tac-toe can be implemented here - we implement R(10, 2, 2) for the default board, for instance, using only one “layer.” It’s not a perfect hash, considering that it doesn’t consider the non-threatened requirement of valid positions, but it is significantly better than a naive hash.