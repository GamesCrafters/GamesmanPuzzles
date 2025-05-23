"""
File: tantrix.py
Puzzle: Tantrix
Author: Abraham Hsu, Grant Zhao, Aditya Tummala
Date: 2025-03-16
"""

from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import ServerPuzzle
from puzzlesolver.players import TUI

class Tantrix(ServerPuzzle):

    id = 'tantrix'
    
    # variants defined as number of pieces, sharp, soft, and straight
    """
    variants = ["3_0_0", "2_2_0", "2_2_1", "2_2_2", "2_4_1", "4_2_2", "4_4_1", "2_6_2", "4_4_2", "5_4_1"]
    """
    variants = ["3_0_0", "2_2_0", "2_2_1", "2_2_2", "2_4_1", "4_2_2", "4_4_1", "2_6_2", "4_4_2", "5_4_1"]
    #             yellow3, red4,   red5,  blue6,   red7,     blue8,    yellow9, red10,    blue10, yellow10
    #                                                                            easy,   medium,    hard
    pieces = ["0_1", "0_2", "0_3", "0_4", "0_5", "1_2", "1_3", "1_4", "1_5", "2_3", "2_4", "2_5", "3_4", "3_5", "4_5"]
    changes = [(0, -3.5), (2.8, -1.7), (2.8, 1.5), (0, 3.1), (-2.8, 1.5), (-2.8, -1.7)]
    """
    coord_change defined as follows:
        (0, -2)  : Up
        (1, -1)  : Top Right
        (1, 1)   : Bottom Right
        (0, 2)   : Down
        (-1, 1)  : Bottom Left
        (-1, -1) : Top Left
    
    Puzzle design defined as follows:
        0: Start position of the line
        1: Sharp turn < to the top right
        2: Soft turn ( to the bottom right
        3: Straight _ to the bottom
        4: Soft turn ) to the bottom left
        5: Sharp turn > to the top left
    """
    coord_change = [(0,-2), (1, -1), (1, 1), (0, 2), (-1, 1), (-1, -1)]

    def __init__(self, variant_id: str, state = [], pieces = [2, 2, 2]):
        """
            Tantrix class will keep a current index tuple (self.curr_index), which maps to coord_change.
            Current index entries will be in mod 6.
            Sharp, soft, and straight lines/curves will define a change in current index, corresponding to board coordinate changes. 
            The first value is the 'head' and the second value is the 'tail' of the path.

            Tantrix class will also keep a current coordinate (self.curr_coord).
            This will be the physical coordinate of the piece on the implicit graph.

            The path will be saved counter-clockwise in self.state
        """
        self.variant_id = variant_id
        self.state = state # Each element in the state is a description of a puzzle piece (coordinate, design) 
                           # Example (0, 0, 1, 4): puzzle is at coordinate (0,0) and has a straight line from from top right to bottom left
        self.num_pieces = sum(pieces)
        self.pieces = pieces # [sharp, soft, straight] number of pieces for each

    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    
    def __hash__(self):
        """ Return a hash value of your position """
        if not self.state:
            return 0
        hash_num = str(self.state[0][2] + 1)
        for state in self.state:
            hash_num += str(state[-1])
        return int(hash_num, base=7)

    def primitive(self, **kwargs):
        """
        Return PuzzleValue.SOLVABLE if the current position is primitive;
        otherwise return PuzzleValue.UNDECIDED.
        """
        #seems good!
        if not self.state:
            return PuzzleValue.UNDECIDED
        
        front_piece = self.state[0] #Takes the very last piece entered into the puzzle from the front
        back_piece = self.state[-1] #Takes the very last piece entered into the puzzle from the back
        change = self.coord_change[back_piece[3]] #Gets the change in coordinates for the back piece
        new_coordx = back_piece[0] + change[0] #Change the coordinates of the last piece
        new_coordy = back_piece[1] + change[1]

        #Check if the new coordinates equal to the front piece and the length of the puzzle is correct
        if ((new_coordx, new_coordy) == (front_piece[0], front_piece[1])):
            if self.num_pieces == 0:
                return PuzzleValue.SOLVABLE
            else:
                return PuzzleValue.UNSOLVABLE
        elif self.num_pieces == 0:
            return PuzzleValue.UNSOLVABLE

        return PuzzleValue.UNDECIDED

    
    def doMove(self, move):
        """
        Return an instance of the puzzle class corresponding to the
        child puzzle position that results from doing the input `move`
        on the current position.
        """
        sharp = self.pieces[0]
        soft = self.pieces[1]
        straight = self.pieces[2]
        if move[1] == 6:
            new_state = deepcopy(self.state)
            piece = new_state.pop(move[0])
            curve = (piece[2] - piece[3] + 6) % 6
            if curve == 1 or curve == 5: #Sharp turns
                sharp = self.pieces[0] + 1
            elif curve == 3: #Straight
                straight = self.pieces[2] + 1
            else: #soft turns
                soft = self.pieces[1] + 1
            return Tantrix(self.variant_id, new_state, [sharp, soft, straight])

        pos = move[0] # pos will be 0 or -1 (head or tail)

        if self.state == []:
            prev = 0 #starting edge
            new_coord = (0, 0) #starting position for first piece
        else:
            prev_state = self.state[pos] #Get the previous piece based on head or tail
            prev_curve = (prev_state[2], prev_state[3]) #start and end of curve in the piece
            prev = (prev_curve[pos] + 3) % 6 #change the end of curve to be correct for the next piece
            change = Tantrix.coord_change[prev_curve[pos]] 
            new_coord = (prev_state[0] + change[0], prev_state[1] + change[1]) #Get the new coords of next piece

        curve = (move[1] - prev + 6) % 6 #Check what type of curve
        
        if curve == 1 or curve == 5: #Sharp turns
            sharp = self.pieces[0] - 1
        elif curve == 3: #Straight
            straight = self.pieces[2] - 1
        else: #soft turns
            soft = self.pieces[1] - 1

        new_state = deepcopy(self.state) # Make a copy of the current state
        new_piece = (new_coord[0], new_coord[1], prev, move[1]) if pos == -1 else (new_coord[0], new_coord[1], move[1], prev)
        insert_pos = len(self.state) if pos == -1 else pos
        new_state.insert(insert_pos, new_piece) # Insert the new piece into the copied state
        return Tantrix(self.variant_id, new_state, [sharp, soft, straight])

    # Returns the coordinates of each existing piece
    def pieceCoords(self): #Helper
        return set([(p[0], p[1]) for p in self.state])
    
    #boolean to check if a design type exists
    def piece_exists(self, start, end): #Helper
        curve = (start-end + 6) % 6
        if (curve == 1 or curve == 5) and self.pieces[0] > 0: #Sharp turns
            return True
        elif curve == 3 and self.pieces[2] > 0: #Straight
            return True
        elif (curve == 2 or curve == 4) and self.pieces[1] > 0: #Soft turns
            return True
        return False

    # Generate Legal Moves & all undo moves
    def generateMoves(self, movetype="all", **kwargs):
        """
        See this link https://github.com/GamesCrafters/GamesmanPuzzles/blob/master/guides/tutorial/02_Moves.md
        to understand what the `movetype` parameter means.
        """
        moves = set() #each element (head or tail of the stack self.state, number 1-5 )
        #If puzzle starts from the very first piece
        
        #Get all moves possible from the head and tail of the board
        if movetype=='for' or movetype=='legal' or movetype=='all':
            if self.state == []:
                if self.pieces[0] > 0:
                    moves = moves.union(set([(0, 1), (0, 5)]))
                if self.pieces[1] > 0:
                    moves = moves.union(set([(0, 2), (0, 4)]))
                if self.pieces[2] > 0:
                    moves = moves.union(set([(0, 3)]))
                return moves #Return all possible moves for the very first piece
            if self.num_pieces == 0:
                return []
            #If both head and tail point to same coordinate, then output one move if that move is available
            head, tail = self.state[0], self.state[-1]
            head_prev, tail_prev = (head[2] + 3) % 6, (tail[3] + 3) % 6  #head_prev = 4, tail_prev = 4
            h_change, t_change = Tantrix.coord_change[head[2]], Tantrix.coord_change[tail[3]] #(1,1), (1, -1)
            h_newcoord, t_newcoord = (head[0]+h_change[0], head[1]+h_change[1]), (tail[0]+t_change[0], tail[1]+t_change[1])
            if h_newcoord == t_newcoord and self.piece_exists(head_prev, tail_prev): #if both head and tail point to same coord
                return [(-1, head_prev)] #add to tail to end the puzzle
            elif h_newcoord == t_newcoord and self.piece_exists(head_prev, tail_prev) == False:
                return list(moves) #return the empty moves as no piece exists to make a legal move
            else: #Get all moves that do not touch another piece
                for curve in range(1, 4): #Do sharp turns and soft turns
                    if self.pieces[curve-1] == 0: #piece has been used up, skip this type of piece
                        continue
                    else:
                        for turn in [-1, 1]: #go clockwise or counterclockwise ex: if start is 4, then we do 3 and then 5
                            h_direction, t_direction = ((turn * curve) + head_prev) % 6, ((turn * curve) + tail_prev) % 6
                            h_newchange, t_newchange = Tantrix.coord_change[h_direction], Tantrix.coord_change[t_direction]
                            h_exist, t_exist = (h_newcoord[0]+h_newchange[0], h_newcoord[1]+h_newchange[1]), (t_newcoord[0]+t_newchange[0], t_newcoord[1]+t_newchange[1])

                            if h_exist not in self.pieceCoords() and h_newcoord not in self.pieceCoords():
                                moves.add((0, h_direction))
                            if t_exist not in self.pieceCoords() and t_newcoord not in self.pieceCoords():
                                moves.add((-1, t_direction))
                #return all possible moves
                return list(moves)
            

        if movetype=='undo' or movetype=='back' or movetype=='all': # backwards.
            if self.state != []:
                return  [(-1, 6), (0, 6)] if self.state != [] else []
            else:
                return []
            
        return moves

    def generateSolutions(self):
        """
        Return a list of instances of the puzzle class where each instance
        is a possible "solved" state of the puzzle.
        """
        return []
    
    @classmethod
    def fromHash(cls, variant_id, hash_val):
        """
        Return an instance of the puzzle class given by the input hash value.
        """
        puzzle = cls(variant_id)
        puzzle.board = hash_val
        return puzzle
    
    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        """
        Return an instance of the Puzzle Class corresponding to the initial position.
        """
        v = variant_id.split("_")
        pieces = [int(i) for i in v]
        return Tantrix(variant_id, pieces = pieces)

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
            curr = []
            parsed_state = []
            neg = False
            for i in position_str:
                if i in ["]", "[", "(", ",", " "]:
                    continue
                elif i == ")":
                    parsed_state.append(tuple(curr))
                    curr = []
                elif i == "-":
                    neg = True
                else:
                    if neg:
                        curr.append(-int(i))
                        neg = False
                    else:
                        curr.append(int(i))
            init_pieces = [0, 0, 0]
            for i in parsed_state:
                curve = (i[2]-i[3] + 6) % 6
                if (curve == 1 or curve == 5): #Sharp turns
                    init_pieces[0] += 1
                elif curve == 3: #Straight
                    init_pieces[2] += 1
                elif (curve == 2 or curve == 4): #Soft turns
                    init_pieces[1] += 1
            total_pieces = [int(variant_id[idx*2]) - init_pieces[idx] for idx in range(len(init_pieces))]
            return Tantrix(variant_id, state=parsed_state, pieces=total_pieces)
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
        if mode == StringMode.AUTOGUI:
            pos_map = {}
            init_x = 5
            init_y = 9
            s = "1_"
            for state in self.state:
                first = min(state[2], state[3])
                second = max(state[2], state[3])
                pos_map[(init_x + state[0], init_y + state[1])] = chr(Tantrix.pieces.index(f"{first}_{second}")+65)

            for j in range(21):
                for i in range(j % 2, 11, 2):
                    s += pos_map.get((i, j), "-")

            if self.pieces[0] != 0:
                s += str(self.pieces[0]) + "A"
            else:
                s += "0P"

            if self.pieces[1] != 0:
                s += str(self.pieces[1]) + "B"
            else:
                s += "0Q"

            if self.pieces[2] != 0:
                s += str(self.pieces[2]) + "C"
            else:
                s += "0R"

            # If the mode is "autogui", return an autogui-formatted position string
            return s
        else:
            # Otherwise, return a human-readable position string.
            return str(self.state)
        
    
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
            # If the mode is "autogui", return an autogui-formatted move string
            pos_map = {}
            init_x = 5
            init_y = 9

            pos = move[0] # pos will be 0 or -1 (head or tail)

            if self.state == []:
                prev = 0 #starting edge
                new_coord = (0, 0) #starting position for first piece
            else:
                prev_state = self.state[pos] #Get the previous piece based on head or tail
                prev_curve = (prev_state[2], prev_state[3]) #start and end of curve in the piece
                prev = (prev_curve[pos] + 3) % 6 #change the end of curve to be correct for the next piece
                change = Tantrix.coord_change[prev_curve[pos]] 
                new_coord = (prev_state[0] + change[0], prev_state[1] + change[1]) #Get the new coords of next piece
            
            new_piece = (new_coord[0], new_coord[1], prev, move[1]) if pos == -1 else (new_coord[0], new_coord[1], move[1], prev)

            new_x = init_x + new_piece[0]
            new_y = init_y + new_piece[1]

            pos_map[(new_x, new_y)] = "found"

            k = 0
            b = False
            for j in range(21):
                for i in range(j % 2, 11, 2):
                    if pos_map.get((i, j), "-") != "-":
                        b = True
                        break
                    else:
                        k += 1
                if b:
                    break

            first_endpoint = f"{k}_{Tantrix.changes[new_piece[2]][0]}_{Tantrix.changes[new_piece[2]][1]}_"
            first_control_point = f"{k}_{Tantrix.changes[new_piece[2]][0]/1.5}_{Tantrix.changes[new_piece[2]][1]/1.5}_"
            second_control_point = f"{k}_{Tantrix.changes[new_piece[3]][0]/1.5}_{Tantrix.changes[new_piece[3]][1]/1.5}_"
            second_endpoint = f"{k}_{Tantrix.changes[new_piece[3]][0]}_{Tantrix.changes[new_piece[3]][1]}_"
            
            return f"LC_RRRR_" + first_endpoint + first_control_point + second_control_point + second_endpoint + "x"
        else:
            # Otherwise, return a human-readable move string.
            return str(move)
    
    #probably useless
    @classmethod
    def isLegalPosition(cls, position_str):
        """Checks if the Puzzle is valid given the rules."""
        state = int(position_str)
        return 0 <= state <= 10 


if __name__ == "__main__":
    t = Tantrix("2_2_2")  # Using the first variant from the variants list
    TUI(t).play()

