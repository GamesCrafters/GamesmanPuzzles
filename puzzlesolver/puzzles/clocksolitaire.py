"""
File: clockSolitaire.py
Puzzle: Clock Solitaire
Author: Divya Sundar, Jennifer Mei-ling Cheng
Date: March 20, 2025
"""
## NEW

from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI


class ClockSolitaire(ServerPuzzle):

    id = 'clocksolitaire'
    variants = ["regular", "pattern4", "pattern7", "pattern10", "pattern12"]
    startRandomized = False

    def __init__(self, variant_id, state = None):
        """
        Your constructor can have any signature you'd like,
        because it is only called by the other methods of this class.
        If your puzzle supports multiple variants, it should
        receive some information on the variant as input.

        An instance of the puzzle class represents a position
        in the puzzle, so the constructor should take in information
        that sufficienctly defines a position as input.
        """
        if state is None:
            state = 0b0111111111111111111
        self.variant_id = variant_id
        self.state = state
        
    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    
    def __hash__(self):
        """ Return a hash value of your position """
        return self.state

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        if (self.variant_id == "regular"):
            if (self.state == 0b1000000000000000000): # need to re-run the database
                return PuzzleValue.SOLVABLE
        elif (self.variant_id == "pattern4"):
            if (self.state == 0b1000000000100010001): # need to re-run the database
                return PuzzleValue.SOLVABLE
        elif (self.variant_id == "pattern10"):
            if (self.state == 0b1010010001000001000):
                return PuzzleValue.SOLVABLE
        elif (self.variant_id == "pattern7"):
            if (self.state == 0b0000000001001001001):
                return PuzzleValue.SOLVABLE
        elif (self.variant_id == "pattern12"):
            if (self.state == 0b1010101001000100010):
                return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
    def doMove(self, move):
        """
        Return an instance of the puzzle class corresponding to the
        child puzzle position that results from doing the input `move`
        on the current position.
        """
        src, dest = move

        # jumping along outer circle
        if ((src >= 0) and (src <= 11)) and ((dest >= 0) and (dest <= 11)):
            d = dest - src
            if d == 2 or d == -10:
                over = (src + 1) % 12
            elif d == -2:
                over = (src - 1) % 12
            elif d == 10:
                over = (dest + 1) % 12

        # jumping in inner circle across center
        elif ((src >= 12) and (src <= 17)) and ((dest >= 12) and (dest <= 17)):
            over = 18
            
        # jumping from outer circle to center
        elif ((src >= 0) and (src <= 11)) and (dest == 18):
            over = (src+1) // 2 + 11
        
        # jumping from center to outer circle
        elif (src == 18) and ((dest >= 0) and (dest <= 11)):
            over = (dest+1) // 2 + 11

        # new_state = self.state.copy()
        # new_state[src] = not(new_state[src])
        # new_state[dest] = not(new_state[dest])
        # new_state[over] = not(new_state[over])

        new_state = self.state ^ (1 << src) ^ (1 << dest) ^ (1 << over)

        return Clock(self.variant_id, new_state)
    

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        moves = []
        key = False

        if movetype=='all':
            key = True

        def has_peg(i):
            return (self.state >> i) & 1
        
        def no_peg(i):
            return not ((self.state >> i) & 1)
        
        if movetype=='for' or movetype=='legal' or key:
            # Moves along outer circumference
            for i in range(12):
                if has_peg(i):
                    if has_peg((i + 1) % 12) and  no_peg((i - 1) % 12):
                        moves.append(((i + 1) % 12, (i - 1) % 12))
                    if has_peg((i - 1) % 12) and no_peg((i + 1) % 12):
                        moves.append(((i - 1) % 12, (i + 1) % 12))

            for i in range(1, 12, 2):
                inner_idx = (i + 1) // 2 + 11
                # Radially inwards moves
                if has_peg(i) and has_peg(inner_idx) and no_peg(18):
                    moves.append((i, 18))
                # Radially outwards moves
                if no_peg(i) and has_peg(inner_idx) and has_peg(18):
                    moves.append((18, i))
            
            # Inner circle moves along diameter
            for i in range(6):
                a = i + 12
                b = (i + 3) % 6 + 12
                if has_peg(18) and has_peg(a) and no_peg(b):
                    moves.append((a, b))

        # dest is full, over is empty, src is empty
        if movetype=='undo' or movetype=='back' or key:
            # Reverse outer circumference moves
            for i in range(12):
                if no_peg(i):
                    if no_peg((i + 1) % 12) and has_peg((i - 1) % 12):
                        moves.append(((i - 1) % 12, (i + 1) % 12))
                    if has_peg((i + 1) % 12) and no_peg((i - 1) % 12):
                        moves.append(((i + 1) % 12, (i - 1) % 12))

            # Reverse radial moves
            for i in range(1, 12, 2):
                inner_idx = (i + 1) // 2 + 11
                if no_peg(i) and no_peg(inner_idx) and has_peg(18):
                    moves.append((18, i))  # undo inward
                if has_peg(i) and no_peg(inner_idx) and no_peg(18):
                    moves.append((i, 18))  # undo outward

            # Reverse inner circle jumps
            for i in range(6):
                a = i + 12
                b = (i + 3) % 6 + 12
                if no_peg(18) and no_peg(a) and has_peg(b):
                    moves.append((b, a))
                
        return tuple(moves)

    def generateSolutions(self):
        """
        Return a list of instances of the puzzle class where each instance
        is a possible "solved" state of the puzzle.
        """
        if (self.variant_id == "regular"):
            return [ClockSolitaire(self.variant_id, 0b1000000000000000000)]
        elif (self.variant_id == "pattern4"):
            return [ClockSolitaire(self.variant_id, 0b1000000000100010001)]
        elif (self.variant_id == "pattern10"):
            return [ClockSolitaire(self.variant_id, 0b1010010001000001000)]
        elif (self.variant_id == "pattern7"):
            return [ClockSolitaire(self.variant_id, 0b0000000001001001001)]
        elif (self.variant_id == "pattern12"):
            return [ClockSolitaire(self.variant_id, 0b1010101001000100010)]


    @classmethod
    def fromHash(cls, variant_id, hash_val):
        """
        Return an instance of the puzzle class given by the input hash value.
        """
        puzzle = cls(variant_id)
        puzzle.state = hash_val
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        """
        Return an instance of the Puzzle Class corresponding to the initial position.
        """
        return Clock(variant_id, 0b0111111111111111111)

    @classmethod
    def fromString(cls, variant_id, position_str):
        """ Given an input human-readable puzzle position string,
        return an instance of the Puzzle Class corresponding to that position.

        Inputs:
            position_str - Human-readable string representation of the puzzle, as given
            by self.toString(StringMode.HUMAN_READABLE)

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        try:
            state = 0
            for i, char in enumerate(position_str.strip()):
                if char.lower() != '-':
                    state |= (1 << i)
            return Clock(variant_id, state)
        except Exception as _:
            raise PuzzleException("Invalid puzzleid")

    def toString(self, mode: StringMode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle position -- String
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE

        def has_peg(i):
            return (self.state >> i) & 1
    
        output = '''\
              O - O - O
            /   \\   /   \\
            O   O   O   O
          /       \\/      \\
          O - O - O - O - O
          \\       /\\      /
           O     O  O    O
            \\   /    \\  /
              O - O - O        
        '''
        row0 = [11, 0, 1]
        row2 = [10, 17, 12, 2]
        row4 = [9, 16, 18, 13, 3]
        row6 = [8, 15, 14, 4]
        row8 = [7, 6, 5]
        row_list = [row0, row2, row4, row6, row8]

        output_str = output.splitlines()
        output_list = [list(line) for line in output_str]

        for i in range(19):
            if has_peg(i):
                for row_i in range(len(row_list)):
                    if i in row_list[row_i]:
                        cell_index = row_list[row_i].index(i)
                        row_index = row_i*2
                    
                        count = -1
                        row = output_list[row_index]
                        for j in range(len(output_list[row_index])):
                            if row[j] == 'O' or row[j] == 'X':
                                count += 1
                                if cell_index == count:
                                    output_list[row_index][j] = 'X'
                                    break

        output_str = '\n'.join([''.join(line) for line in output_list])

        if mode == StringMode.AUTOGUI:
            # If the mode is "autogui", return an autogui-formatted position string
            return '1_' + ''.join(['x' if has_peg(i) else '-' for i in range(19)])
        elif mode == StringMode.HUMAN_READABLE_MULTILINE:
            return output_str
        else:
            # Otherwise, return a human-readable position string.
            return ''.join(['x' if has_peg(i) else '-' for i in range(19)])
        
    
    def moveString(self, move, mode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the move -- String
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE
        if mode == StringMode.AUTOGUI:
            return f'M_{move[0]}_{move[1]}_x'
        else:
            return f'{move[0]} → {move[1]}'
    
    @classmethod
    def isLegalPosition(cls, position_str):
        """Checks if the Puzzle is valid given the rules."""
        return True

# p = Clock("regular")
# TUI(p, solver=GeneralSolver(p), info=True).play()


# xxxxxx-xxxxxxxxxx-x