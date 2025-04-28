from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI


class EightBall(Puzzle):
    id = None
    variants = None
    startRandomized = None

    # size cannot be changed
    size = 3
    midRowPos = [3, 4, 5]
    winning_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    def __init__(self, **kwargs):
        # positions represented as a 1D list - ex) [1, 2, 3, 4, 5, 6. 7, 8, 0]
        # underlying structure:
        # Todo
        self.position = [i for i in range(1, self.size**2)] + [0]

    @property
    def variant(self):
        pass

    def __hash__(self):
        pass

    def __str__(self):
        pass

    # Done? I guess?
    def primitive(self):
        if self.position == self.winning_state:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def doMove(self, move):
        print(move)
        print(isinstance(move, list))
        # check if the move is either a tuple or a list of tuples
        if not isinstance(move, tuple) and not isinstance(move, list): raise TypeError
        # check specific conditions for when the move is a tuple (one swap)
        if isinstance(move, tuple):
            if (len(move) != 2 
                or not isinstance(move[0], int)
                or not isinstance(move[1], int)
            ):
                raise TypeError
        # check specific conditions for when the move is a list of tuples (two swaps) - e.g., [(1,2),(0,1)]
        if isinstance(move, list):
            if (len(move) != 2 
                or not isinstance(move[0], tuple)
                or not isinstance(move[1], tuple)
                or not isinstance(move[0][0], int)
                or not isinstance(move[0][1], int)
                or not isinstance(move[1][0], int)
                or not isinstance(move[1][1], int)
            ):
                raise TypeError
        # Check if move is a valid move
        if move not in self.generateMoves(): raise ValueError
        
        # Create a new puzzle (currently have default positions)
        newPuzzle = EightBall()
        # if move is a tuple
        if isinstance(move, tuple):
            newPuzzle.position = EightBall.swap(self.position[:], move[0], move[1])
        else: # if move is a list of two tuples
            newPuzzle.position = EightBall.doubleSwap(self.position[:], move)

        return newPuzzle
    
    @staticmethod
    def swap(arr, i1, i2):
        arr[i1], arr[i2] = arr[i2], arr[i1]
        return arr
    
    @staticmethod
    def doubleSwap(position, moveList): # moveList contains two tuples - e.g., [(1,2),(0,1)]
        firstMove = moveList[0]
        secondMove = moveList[1]

        position = EightBall.swap(position, firstMove[0], firstMove[1])
        position = EightBall.swap(position, secondMove[0], secondMove[1])

        return position

    def generateMoves(self, movetype='bi', **kwargs):
        if movetype in ['for', 'back']:
            return []  # Block unwanted move types

        index_0 = self.position.index(0)  # Find the empty tile
        moveList = []

        # Get adjacent positions
        adj_positions = []
        if index_0 - 3 >= 0:  # Move UP
            adj_positions.append(index_0 - 3)
        if index_0 + 3 < 9:  # Move DOWN
            adj_positions.append(index_0 + 3)
        # if 0 is not in the middle row
        if index_0 // 3 != 1:
            if index_0 % 3 != 0:  # Move LEFT
                adj_positions.append(index_0 - 1)
            if index_0 % 3 != 2:  # Move RIGHT
                adj_positions.append(index_0 + 1)

        # **Single Swaps**
        for pos in adj_positions:
            moveList.append((pos, index_0))  # Swap this tile with `0`

        # **Two-Swaps (Sliding Two Tiles)**
        if index_0 // 3 == 0:  # If `0` is in row 0, check DOWNWARD two swaps
            if index_0 + 6 < 9:
                moveList.append([(index_0 + 3, index_0), (index_0 + 6, index_0 + 3)])
        if index_0 // 3 == 2:  # If `0` is in row 2, check UPWARD two swaps
            if index_0 - 6 >= 0:
                moveList.append([(index_0 - 3, index_0), (index_0 - 6, index_0 - 3)])

        # if 0 is not in the middle row
        if index_0 // 3 != 1:
            if index_0 % 3 == 0:  # If `0` is in col 0, check RIGHT two swaps
                if index_0 + 2 < 9:
                    moveList.append([(index_0 + 1, index_0), (index_0 + 2, index_0 + 1)])
            if index_0 % 3 == 2:  # If `0` is in col 2, check LEFT two swaps
                if index_0 - 2 >= 0:
                    moveList.append([(index_0 - 1, index_0), (index_0 - 2, index_0 - 1)])

        return moveList

    # Done? I guess?
    def generateSolutions(self):
        newPuzzle = EightBall()
        newPuzzle.position = self.winning_state
        return [newPuzzle]
    
    def toString(self, **kwargs):
        grid = self.position
        return f"0:{grid[0]}  1:{grid[1]}  2:{grid[2]}\n" \
           f"3:{grid[3]} |4:{grid[4]}| 5:{grid[5]}\n" \
           f"6:{grid[6]}  7:{grid[7]}  8:{grid[8]}"

    def moveString(self, move, mode):
        pass

    @classmethod
    def isLegalPosition(self):
        pass

TUI(EightBall()).play()