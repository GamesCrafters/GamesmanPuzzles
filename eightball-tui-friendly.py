from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI


class EightBall(Puzzle):
    id = "eightball"
    variants = 'regular'
    startRandomized = False

    # size cannot be changed
    size = 3
    midRowPos = [3, 4, 5]
    winning_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    def __init__(self, **kwargs):
        # positions represented as a 1D list - ex) [1, 2, 3, 4, 5, 6. 7, 8, 0]
        # underlying structure:
        # Todo
        # self.position = [i for i in range(1, self.size**2)] + [0]
        self.position = [5, 7, 3, 4, 6, 0, 2, 8, 1]

    @property
    def variant(self):
        pass

    def __hash__(self):
        return hash(tuple(self.position))

    def __str__(self):
        pass

    # Done? I guess?
    def primitive(self):
        if self.position == self.winning_state:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        # check if the move is either a tuple or a list of tuples
        if not isinstance(move, tuple) and not isinstance(move, list): raise TypeError
        # check specific conditions for when the move is a tuple (one swap)
        if isinstance(move, tuple) and isinstance(move[0], int):
            if (len(move) != 2 
                or not isinstance(move[0], int)
                or not isinstance(move[1], int)
            ):
                raise TypeError
        # check specific conditions for when the move is a list of tuples (two swaps) - e.g., [(1,2),(0,1)]
        if isinstance(move, tuple) and isinstance(move[0], tuple):
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
        if isinstance(move, tuple) and isinstance(move[0], int):
            newPuzzle.position = EightBall.swap(self.position[:], move[0], move[1])
        else: # if move is a list of two tuples
            newPuzzle.position = EightBall.doubleSwap(self.position[:], move)

        return newPuzzle
    
    @staticmethod
    def swap(arr, v1, v2): # v = value
        # find the index of each value
        i1, i2 = arr.index(v1), arr.index(v2)
        arr[i1], arr[i2] = arr[i2], arr[i1]
        return arr
    
    @staticmethod
    def doubleSwap(position, moveList): # moveList contains two tuples - e.g., [(1,2),(0,1)]
        firstMove = moveList[0] #(2,0)
        secondMove = moveList[1]

        i1 = position.index(firstMove[0]) # index of the first value of the first tuple(move)
        i2 = position.index(firstMove[1])
        i3 = position.index(secondMove[0]) # index of the first value of the second tuple(move)

        # i1 swpped with i2, i3 swapped with i1
        position[i1], position[i2] = position[i2], position[i1]
        position[i3], position[i1] = position[i1], position[i3]

        return position

    def generateMoves(self, movetype='bi', **kwargs):
        if movetype in ['for', 'back']:
            return []  # Block unwanted move types
        
        posList = self.position
        index_0 = posList.index(0)  # Find the index of the empty ball
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
            moveList.append((posList[pos], posList[index_0]))  # Swap this tile with `0`

        # **Two-Swaps (Sliding Two Tiles)**
        if index_0 // 3 == 0:  # If `0` is in row 0, check DOWNWARD two swaps
            if index_0 + 6 < 9:
                moveList.append(((posList[index_0 + 3], posList[index_0]), (posList[index_0 + 6], posList[index_0 + 3])))
        if index_0 // 3 == 2:  # If `0` is in row 2, check UPWARD two swaps
            if index_0 - 6 >= 0:
                moveList.append(((posList[index_0 - 3], posList[index_0]), (posList[index_0 - 6], posList[index_0 - 3])))

        # if 0 is not in the middle row
        if index_0 // 3 != 1:
            if index_0 % 3 == 0:  # If `0` is in col 0, check RIGHT two swaps
                if index_0 + 2 < 9:
                    moveList.append(((posList[index_0 + 1], posList[index_0]), (posList[index_0 + 2], posList[index_0 + 1])))
            if index_0 % 3 == 2:  # If `0` is in col 2, check LEFT two swaps
                if index_0 - 2 >= 0:
                    moveList.append(((posList[index_0 - 1], posList[index_0]), (posList[index_0 - 2], posList[index_0 - 1])))

        return moveList

    # Done? I guess?
    def generateSolutions(self):
        newPuzzle = EightBall()
        newPuzzle.position = self.winning_state
        return [newPuzzle]
    
    def toString(self, **kwargs):
        grid = self.position
        return f"{grid[0]}  {grid[1]}  {grid[2]}\n" \
           f"{grid[3]} |{grid[4]}| {grid[5]}\n" \
           f"{grid[6]}  {grid[7]}  {grid[8]}"
    
    def toString(self, mode):
        prefix = '1_' if mode == StringMode.AUTOGUI else ''
        return prefix + ''.join([str(x) if int(x) != 0 else '-' for x in self.position])

    # arrow representation (hopefully)
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            # if move is a single slide
            if isinstance(move[0], int):
                return f'M_{move[0]}_{move[1]}_x'
            # if move is a double slide
            if isinstance(move[0], tuple):
                return f'M_{move[1][0]}_{move[0][1]}_x'


    # def moveString(self, move, mode):
    #     if mode == StringMode.AUTOGUI:
    #         return f'M_{move[0]}_{move[1]}_x'
    #     else:
    #         return str(self.position[move[0]])

    @classmethod
    def isLegalPosition(self):
        pass

p = EightBall()
TUI(p,GeneralSolver(p), info=True).play()