"""
File: sevenpennies.py
Puzzle: Seven Pennies
Author: Jerry Fang (Backend), Zacky Huang (Backend), Alvaro Estrella (Mentor), Abraham Hsu (GamesmanPuzzles Debugging)
Date: 2025-03-17
"""

from copy import deepcopy
from ..util import *
from ..puzzles import ServerPuzzle
from ..solvers import GeneralSolver
from ..players import TUI


TWO_TO_THE_ = [1,2,4,8,16,32,64,128,256,512,1024,2048]

class SevenPennies(ServerPuzzle):
    # This ID is used when you run in your terminal python3 tui.py {puzzle_id}
    id = 'sevenpennies'
    variants = ['regular']

    # lastPennyPlacedIndex is an integer [0-7] when last move is a sliding move
    # lastPennyPlacedIndex is an '-1' when next move is adding a penny
    def __init__(self, position = [0,0,0,0,0,0,0,0], lastPennyPlacedIndex = -1, _variant_id = 'regular', **kargs):
        self.position = position
        self.lastPennyPlacedIndex = lastPennyPlacedIndex
        self._variant_id = _variant_id

    
    def primitive(self, **kargs):
        #Returns SOLVABLE when Player has placed all 7 coins and last move is slide move (lastPennyPlacedIndex == -1)
        if self.lastPennyPlacedIndex == -1:
            if sum(self.position) == 7:
                return PuzzleValue.SOLVABLE
        #Returns UNSOLVABLE when Player cannot slide the most recently penny placed.
        if (self.lastPennyPlacedIndex != -1 and 
            self.position[(self.lastPennyPlacedIndex +3) %8] ==1 and 
            self.position[(self.lastPennyPlacedIndex +5) %8] ==1):
            return PuzzleValue.UNSOLVABLE
        return PuzzleValue.UNDECIDED
    

    def generateMoves(self, movetype="for", **kargs):
        moves = []

        #Return empty list if move type is not for, legal, undo
        if (movetype != "for" and movetype != "legal" and movetype != "undo"):
            return moves
        
        if movetype == "undo":    
            # If a penny was added in the last move, adds the undo move to the move list
            if self.lastPennyPlacedIndex != -1:
                moves.append((-self.lastPennyPlacedIndex,"u"))  
                return moves            
            # Else, if a penny was slid in the last move
            else:
                for i in range(8):
                    if self.position[i] == 1: 
                        #Generate all possible undo slide route.
                        node1 = (i + 3) % 8
                        node2 = (i + 5) % 8
                        # If a slot is filled and the interconnect slots with the slot is empty,
                        # we count the route between the two slots as a valid undo route
                        if self.position[node1] == 0: 
                            moves.append((-node1, -i,"u")) 
                        if self.position[node2] == 0:
                            moves.append((-node2, -i,"u")) 
            return moves
        
        #If last move was a place move, adds all sliding moves for that penny
        elif (self.lastPennyPlacedIndex >= 0 and self.lastPennyPlacedIndex < 8): 
            
            #Node 1, 2 are slots interconnected with the lastPennyPlacedIndex slot on the board
            node1 = (self.lastPennyPlacedIndex + 3) % 8
            node2 = (self.lastPennyPlacedIndex + 5) % 8

            #If Node 1, Node 2 is empty, return the route from lastPennyPlaceIndex to Node 1, Node 2
            if (self.position[node1] == 0):
                moves.append((self.lastPennyPlacedIndex, node1))
            if (self.position[node2] == 0):
                moves.append((self.lastPennyPlacedIndex, node2))
            return moves
        
        else:
            #If there are 7 pennies on the board, returns an empty list
            if sum(self.position) == 7:
                return moves
            
            #Returns all empty slot(s) on the board
            for i in range(8): 
                if (self.position[i] == 0):
                    moves.append((i,))             
            return moves

    def doMove(self, move, **kargs):
        newPosition = deepcopy(self.position)
        newLastPennyPlaced = -1

        #Check if the current move is an undo move
        isUndo = (move[-1] == "u")
        if isUndo:
            #Removes the penny from board
            if len(move) == 2:
                takePenny = -move[0]
                newPosition[takePenny] = 0

            #Slides the penny back
            else:
                start = -move[0]
                end = -move[1]
                newPosition[start] = 1
                newPosition[end] = 0
                newLastPennyPlaced = start

        #Handles forward moves
        else:
            if len(move) != 1:#If the move is a sliding move
                startPosition, endPosition = move
                newPosition[(startPosition%8)] = 0
                newPosition[(endPosition%8)] = 1
                #Sets the lastPennyPlacedIndex as slid
                newLastPennyPlaced = -1
                
            else:
                (newPenny,) = move
                newPosition[(newPenny%8)] = 1
                #Sets the lastPennyPlacedIndex to the current penny
                newLastPennyPlaced = newPenny

        return SevenPennies(position=newPosition,lastPennyPlacedIndex=newLastPennyPlaced, _variant_id='regular')
    
    def moveString(self, move, mode):
        if mode == StringMode.AUTOGUI:
            if len(move) == 1: #Forward placing move
                if move[0] >= 0:
                    return f"A_-_{(move[0]%8)}_y"
                else:
                    return f"A_-_{(-move[0]%8)}_y"
            else:
                if move[0] >= 0:#Forward sliding move
                    return f"M_{(move[0]%8)}_{(move[1]%8)}_x"
                else:
                    return f"M_{(-move[0]%8)}_{(-move[1]%8)}_x"
    
        if move[-1] == "u":#Undo move
            if len(move) == 2:#Remove move
                return f"Undo {-move[0]}"
            else:#Undo sliding move
                return f"Undo {-move[0]} -> {-move[1]}"
        else:#Forward move
            if len(move) == 1:#Placing move
                return f"{move[0]}"
            else:#Sliding move
                return f"{move[0]} -> {move[1]}"

    def toString(self, mode, **kargs):
        if mode == StringMode.AUTOGUI:
            posString = '1_'

            #Iterates through all place in board.
            #if place is filled, adds 'p', else adds '-'
            for pos in self.position:
                if pos == 1:
                    posString += "p"
                else:
                    posString += "-"
    
            #Keeps track of last move, 
            #if a penny was added appends the penny index,
            #else if a penny was slid appends '_9'
            if self.lastPennyPlacedIndex == -1:
                posString += "_9"
            else:
                posString += f"_{self.lastPennyPlacedIndex}"
            return posString

        elif mode == StringMode.HUMAN_READABLE:
            returnPos = ""
            #Iterates through all place in board.
            #if place is filled, adds '1', else adds '0'
            for pos in self.position:
                if pos == 1:
                    returnPos += "1"
                else:
                    returnPos += "0"
            #Keeps track of last move, 
            #if a penny was added appends the penny index,
            #else if a penny was slid appends '_9'
            if self.lastPennyPlacedIndex == -1:
                returnPos += "_9"
            else:
                returnPos += f"_{self.lastPennyPlacedIndex}"
            return returnPos
            
        #TUI
        return f"""
    {'*' if self.position[0] == 1 else 0}   {'*' if self.position[1] == 1 else 1}    
    |\\ /|    
    | \\ |    
    |/ \\|    
{'*' if self.position[7] == 1 else 7}---|---|---{'*' if self.position[2] == 1 else 2}
 \\ /|   |\\ / 
  / |   | \\  
 / \\|   |/ \\ 
{'*' if self.position[6] == 1 else 6}---|---|---{'*' if self.position[3] == 1 else 3}
    |\\ /|    
    | \\ |    
    |/ \\|    
    {'*' if self.position[5] == 1 else 5}   {'*' if self.position[4] == 1 else 4}    
"""
    


    def __hash__(self, **kargs):
        bitPattern = ""
        if (self.lastPennyPlacedIndex != -1):
            bitPattern = f"{int(self.lastPennyPlacedIndex):04b}"
        else:
            bitPattern = "1001"

        bitPattern = bitPattern + ''.join((str(x) for x in self.position))
        return int(bitPattern, base=2)
    
    @classmethod
    def fromHash(cls, hashValue, **kargs):
        bitPattern = ""

        remainingValue = hashValue
        for power in reversed(range(12)):
            if remainingValue >= TWO_TO_THE_[power]:
                remainingValue -= TWO_TO_THE_[power]
                bitPattern = '1' + bitPattern
            else:
                bitPattern = '0' + bitPattern
        
        decodedLastPennyPlacedIndex = int(bitPattern[:4], base=2)
        lastPennyPlacedIndex = -1 if decodedLastPennyPlacedIndex == 9 else decodedLastPennyPlacedIndex

        position = [int(bit) for bit in bitPattern[4:]]
        return SevenPennies(position=position, lastPennyPlacedIndex=lastPennyPlacedIndex, _variant_id='regular')
    
    @classmethod
    def fromString(cls, variant_id, position_str):
        boardPosition = []
        lastPenny = position_str[-1]
        for pos in position_str[0:9]:
            if pos == "0":
                boardPosition.append(0)
            elif pos == "1":
                boardPosition.append(1)
        lastPenny = -1 if lastPenny == "9" else int(lastPenny)
        puzzle = cls(boardPosition,lastPenny,_variant_id = 'regular')
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        return SevenPennies(position=[0,0,0,0,0,0,0,0],lastPennyPlacedIndex=-1, _variant_id= variant_id)

    @property
    def variant(self):
        return self._variant_id     
