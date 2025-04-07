"""
File: tiltago.py
Puzzle: Tiltago
Author: Nakul Srikanth, Bella Longhi, Talha Ijaz
Date: March 10, 2025
Description: TODO
"""
from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import GeneralSolver
from puzzlesolver.players import TUI

from puzzlesolver.puzzles import ServerPuzzle

class Tiltago(ServerPuzzle):
    id = "tiltago"
    variants = ["regular"]

    def __init__(self, variant, position=None):
        self._var = variant
        # p, direction = variant.split("_")
        if variant not in self.variants:
            raise ValueError(f"Invalid variant: {variant}")
        if position is not None:
            self._pos = position
            self._start = position
        else:
            self._start = "5-B-4B213"
            self._pos = "5-B-4B213"
            
        self.lookup_table = {0:[1], 1:[0,4], 2:[3], 3:[2, 4], 4:[1,3,5, 7], 5:[4,6], 6:[5],
                             7:[4,8], 8:[7]}

    def __hash__(self):
        return hash(self._pos)
    
    @classmethod
    def getBoard(self, pos):
        final = ""
        for i in range(2):
            final = final + "  " + pos[i] + "\n"
        for i in range(2, 7):
            final = final + pos[i]
        final += "\n"
        for i in range (7, 9):
            final = final + "  " + pos[i] + "\n"
        return final


    def toString(self, mode):
        if mode == StringMode.AUTOGUI:
            variant_size = int(self._var.split('_')[0])
            string_length = variant_size + 1  # Include positions 0 to variant_size
            result = ['-'] * string_length
            
            result[self._pos] = '1'
            position_str = ''.join(result)
            
            return f"1_{position_str}"

        return self.getBoard(self._pos)

    @classmethod
    def generateStartPosition(self, variant, **kwargs):
        return Tiltago(variant)

    @classmethod
    def fromString(self, variant, position_str):
        if not isinstance(position_str, str):
            raise TypeError("Position string must be a string")
        if position_str == "":
            return self.generateStartPosition(variant)
        if variant not in self.variants:
            raise ValueError("Invalid variant")
        pos = position_str
        return Tiltago(variant, pos)

    # def bidirectional_moves(self, movetype="all"):
    #     # Written a general solver, however, wanted to see case-by-case for debugging purposes.
    #     # Will keep this for the time-being, if user is interested in writting general solver, then by all means, go for it.
    #     # 
    #     # 
    #     # Here is some observations if interested (don't read if you're interested on solving yourself).
    #       # Hard code start, 0 and 1. Then every pos % 3 == 0 should return -1.
    #       # Then pos % 3 == 1 will be forward_moves + [(-1,)] and pos % 3 == 2 will be backward_moves + forward_moves.
    #       # Since 5 is pos % 4 == 1, we'll have to ensure when this happens, we don't return backward_moves + forward_moves.
    #       #
    #       #
    #       # E.G.
    #     """
    #       if self._pos != 0 and self._pos % 3 == 0:
    #           return [(-1,)]
    #       elif self._pos >= self._start:
    #           return [(1,), (2,)]
    #       if (self._pos + 2) % 3 == 0:
    #           return [(-1,), (1,)] if self._pos % 4 == 1 else [(-1,), (1,), (2,)]
    #       elif (self._pos + 1) % 3 == 0:
    #           return [(-2,), (1,)] if self._pos % 4 == 1 else [(-2,), (1,), (2,)]
    #       return [(-2,), (-1,), (1,), (2,)]
    #     """
    #     # something like this would suffice.
    #     if movetype in ["for", "back"]:
    #         return []
    #     backward_moves = [-2, -1]
    #     forward_moves = [1, 2]
    #     cases = {
    #         "4_bi": {
    #             4: forward_moves,
    #             3: [-1],
    #             2: [-2] + forward_moves,
    #             1: [-1] + [1],
    #             0: backward_moves
    #         },
    #         "10_bi": {
    #             10: forward_moves,
    #             9: [-1],
    #             8: [-2] + forward_moves,
    #             7: [-1] + forward_moves,
    #             6: backward_moves,
    #             5: [-2] + [1],
    #             4: [-1] + forward_moves,
    #             3: [-1],
    #             2: [-2] + forward_moves,
    #             1: [-1] + [1],
    #             0: backward_moves
    #         }
    #     }
    #     return cases.get(self._var, {}).get(self._pos, [])

    # def forward_moves(self, movetype):
    #     if movetype == "undo":
    #         if self._pos == 1:
    #             return [-1]
    #         elif self._pos == 0:
    #             return [-1, -2]
    #         elif self._pos == 3:
    #             return [-1]
    #         elif self._pos == 2:
    #             return [-2]
    #         return []
    #     else:
    #         if self._pos % 4 == 1:
    #             return [1]
    #         elif self._pos == 4:
    #             return [1, 2]
    #         elif self._pos == 2:
    #             return [1, 2]
    #         return []

    def generateMoves(self, movetype='legal'):
        return_gen_moves_dict = []
        for i in range(9):
            if self._pos[i] != "-":
                for j in self.lookup_table[i]:
                    if self._pos[j] == '-':
                        return_gen_moves_dict.append((i, j))    
                        
        return return_gen_moves_dict
                
    def doMove(self, move):
        i, j = move[0], move[1]
        s_list = list(self._pos)
        s_list[i], s_list[j] = s_list[j], s_list[i]
        new_pos = ''.join(s_list)
        return Tiltago(self._var, new_pos)

    def moveString(self, move, mode):
        """Convert integer move to human-readable string for output."""
        if mode == StringMode.AUTOGUI:
            to_position = self._pos
            to_position -= move 
            return f"M_{self._pos}_{to_position}_y"
        if move > 0: return f"Take {move}"
        else: return f"Add {-move}"

    def primitive(self):
        if self._pos == 'B--12345--B':
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED
    
        """ if self._dir == "bi":
            if self._pos == 0:
                return PuzzleValue.SOLVABLE
            return PuzzleValue.UNDECIDED
        elif self._dir == "for":
            if self._pos == 0:
                return PuzzleValue.SOLVABLE
            elif self._pos % 3 == 0:
                return PuzzleValue.UNSOLVABLE
            return PuzzleValue.UNDECIDED """

    def generateSolutions(self, **kwargs):
        new_puzzle = Tiltago(self._var)
        new_puzzle._pos = 'B-1234567-B'
        return [new_puzzle]

    @property
    def variant(self):
        return self._var

if __name__ == "__main__":
    # from scripts.server.src import test_puzzle
    # test_puzzle(Tiltago)
    puzzle = Tiltago("regular")
    TUI(puzzle).play()

