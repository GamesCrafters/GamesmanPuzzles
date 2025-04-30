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
            self._start = "----53241"
            self._pos = "----53241"
            
        # self.lookup_table = {0:[1], 1:[0,2], 2:[1,6], 3:[4], 4:[3,5], 5:[4,6], 6:[2,5,7,10],
        #                      7:[6,8], 8:[7,9], 9:[8], 10:[6,11], 11:[10,12], 12:[11]}

        """
            0
            1
          23456
            7
            8
        """
        self.lookup_table = {0:[1], 1:[0,4], 2:[3], 3:[2,4], 4:[1,3,5,7], 5:[4,6], 6:[5],
                             7:[4,8], 8:[7]}

    def __hash__(self):    
        import hashlib
        mod=100000
        hashed = hashlib.sha256(self._pos.encode()).hexdigest()
        return int(hashed, 16) % mod
    
    @classmethod
    def getBoard(self, pos):
        final = ""
        for i in range(2):
            final = final + "   " + pos[i] + "\n"
        for i in range(5):
            final = final + pos[3 + i]
        final += "\n"
        for i in range (7, 9):
            final = final + "   " + pos[i] + "\n"
        return final


    def toString(self, mode):
        if mode == StringMode.AUTOGUI:            
            return f"1_{self._pos}"
        elif mode == StringMode.HUMAN_READABLE:
            return self._pos
        elif mode == StringMode.HUMAN_READABLE_MULTILINE:
            return self.getBoard(self._pos)

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
    
    def generateMoves(self, movetype="all"):
        if movetype=='for' or movetype=='back': return []
        
        moves = []
        occupied = set(i for i in range(9) if self._pos[i] != "-")

        for start in occupied:
            if start == 4:
                # Ball is already at center, only need to generate center moves later
                continue

            # Check if we can reach center (node 4)
            visited = set()
            stack = [start]
            can_reach_center = False

            while stack:
                current = stack.pop()
                if current == 4:
                    can_reach_center = True
                    break
                for neighbor in self.lookup_table[current]:
                    if neighbor not in visited and self._pos[neighbor] == "-":
                        visited.add(neighbor)
                        stack.append(neighbor)

            if can_reach_center:
                moves.append((start, 4))  # Only allow start → 4 move first

        # Now, for balls already at center (4), find all reachable empty slots
        if self._pos[4] != "-":
            visited = set()
            stack = [4]

            while stack:
                current = stack.pop()
                for neighbor in self.lookup_table[current]:
                    if neighbor not in visited and self._pos[neighbor] == "-":
                        moves.append((4, neighbor))
                        visited.add(neighbor)
                        stack.append(neighbor)

        return moves
                
    def doMove(self, move):
        start, end = move
        s_list = list(self._pos)
        s_list[end] = s_list[start]  # move ball to destination
        s_list[start] = '-'          # empty original spot
        new_pos = ''.join(s_list)
        return Tiltago(self._var, new_pos)

    def moveString(self, move, mode):
        """Convert integer move to human-readable string for output."""
        if mode == StringMode.AUTOGUI:
            before, after = move
            return f"M_{before}_{after}_x"
        
        return move

    def primitive(self):
        if self._pos == "--12345--":
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def generateSolutions(self, **kwargs):
        new_puzzle = Tiltago(self._var)
        new_puzzle._pos = '--12345--'
        return [new_puzzle]

    @property
    def variant(self):
        return self._var

if __name__ == "__main__":
    # from scripts.server.src import test_puzzle
    # test_puzzle(Tiltago)
    puzzle = Tiltago("regular")
    # TUI(puzzle).play()
    solver = GeneralSolver(puzzle)
    solver.solve(verbose=True)

