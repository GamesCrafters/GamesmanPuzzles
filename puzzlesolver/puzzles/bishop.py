from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import IndexSolver
import math

class Bishop(ServerPuzzle):
	# For simplicity, only one color of square is considered.
	puzzleid = 'bishop'
	author = 'Brian Delaney'
	name = 'Bishop Puzzle'
	description = """Swap the locations of two sets of bishops on opposite ends of a chessboard, without moving them into threatened positions."""
	date_created = "October 30, 2020"
	# Chessboard has y rows, 2x columns
	variants = {str(i[0]) + "x" + str(i[1]): IndexSolver for i in ((2,5), (2,7), (3,7))}
	test_variants = {str(i[0]) + "x" + str(i[1]): IndexSolver for i in ((2,5), (2,7))}
	
	def __init__(self, bishops=2, rows=5, **kwargs):
		# The bottom left square has a bishop.
		# The arrays are: [row, col]
		self.rows = rows
		self.cols = bishops * 2
		self.black = [(0, 2*i) for i in range(bishops)]
		self.white = [(rows - 1, 2*i + 1 - (rows % 2)) for i in range(bishops)]
		
	def __str__(self, **kwargs):
		"""Returns the string representation of the puzzle.
        
        Outputs:
            String representation -- String
        """
		arr = [["*" if (i+j) % 2 == 0 else "." for i in range(self.cols)] for j in range(self.rows)]
		for w in self.white:
			arr[w[0]][w[1]] = "W"
		for b in self.black:
			arr[b[0]][b[1]] = "B"
		return "\n".join([str(arr2) for arr2 in arr])
		
	@property
	def variant(self):
		return str(self.cols // 2) + "x" + str(self.rows)
		
	def primitive(self, **kwargs):
		"""If the Puzzle is at an endstate, return PuzzleValue.SOLVABLE
        else return PuzzleValue.UNDECIDED

        Note that the original description references GameValue, which
        are not found in the util.py file (in this build).

        Outputs:
            Primitive of Puzzle type PuzzleValue
        """
		for w in self.white:
			if w[0] != 0:
				return PuzzleValue.UNDECIDED
		for b in self.black:
			if b[0] != self.rows - 1:
				return PuzzleValue.UNDECIDED
		return PuzzleValue.SOLVABLE
		
	def generateMoves(self, movetype='all', **kwargs):
		"""Generate moves from self (including undos)

        Inputs
            movetype -- str, can be the following
            - 'for': forward moves
            - 'bi': bidirectional moves
            - 'back': back moves
            - 'legal': legal moves (for + bi)
            - 'undo': undo moves (back + bi)
            - 'all': any defined move (for + bi + back)

        Outputs:
            Iterable of moves, move must be hashable
        """
		if movetype == 'for' or movetype == 'back':
			return []
		moves, moves_raw = [], []
		dest_w, dest_b = set(), set()
		# Generate all possible moves; check for intersection later
		for w in self.white:
			self.checkDiagonal(w, 1, 1, moves_raw, dest_w)
			self.checkDiagonal(w, 1, -1, moves_raw, dest_w)
			self.checkDiagonal(w, -1, 1, moves_raw, dest_w)
			self.checkDiagonal(w, -1, -1, moves_raw, dest_w)
		for b in self.black:
			self.checkDiagonal(b, 1, 1, moves_raw, dest_b)
			self.checkDiagonal(b, 1, -1, moves_raw, dest_b)
			self.checkDiagonal(b, -1, 1, moves_raw, dest_b)
			self.checkDiagonal(b, -1, -1, moves_raw, dest_b)
		# Find valid moves, postprocess into nice notation
		dest_valid = dest_w ^ dest_b # Symmetric difference
		conv = lambda num: chr(num + 97)
		for move in moves_raw:
			dest = (move[2], move[3])
			if dest in dest_valid:
				moves.append((conv(move[1]) + str(self.rows - move[0]),\
				conv(move[3]) + str(self.rows - move[2])))
		moves.sort(key = lambda tup: tup[0][::-1] + tup[1][::-1])
		return moves
		
	def checkDiagonal(self, s, x, y, moves, dest):
		"""
		Helper method that generates moves in one diagonal direction for
		one piece. Adds moves generated to moves and destination spaces to dest.
		"""
		i = 1
		new = (s[0] + x, s[1] + y)
		while new[0] >= 0 and new[1] >= 0 \
		and new[0] < self.rows and new[1] < self.cols \
		and new not in self.white and new not in self.black:
			moves.append((s[0], s[1], new[0], new[1]))
			dest.add(new)
			new = (new[0] + x, new[1] + y)
		
	def doMove(self, move, **kwargs):
		"""Given a valid move, returns a new Puzzle object with that move executed.
        Does nothing to the original Puzzle object

        Inputs:
            move -- type defined by generateMoves

        Outputs:
            Puzzle with move executed
        """
		if move not in self.generateMoves():
			raise ValueError
		deconv = lambda c: ord(c) - 97
		src = (self.rows - int(move[0][1]), deconv(move[0][0]))
		dest = (self.rows - int(move[1][1]), deconv(move[1][0]))
		new_white, new_black = deepcopy(self.white), deepcopy(self.black)
		if src in new_white:
			new_white.remove(src)
			new_white.append(dest)
		elif src in new_black:
			new_black.remove(src)
			new_black.append(dest)
		newPuzzle = Bishop(bishops = self.cols // 2, rows = self.rows)
		newPuzzle.white = new_white
		newPuzzle.black = new_black
		return newPuzzle
		
	def __hash__(self):
		"""Returns a hash of the puzzle.
        Requirements:
        - Each different puzzle must have a different hash
        - The same puzzle must have the same hash.
        
        Outputs:
            Hash of Puzzle -- Integer
        """
		hArray = []
		posMap = {}
		index = 0
		for r in range(self.rows):
			for c in range(0,self.cols,2):
				hArray.append(0)
				posMap[(r, c+(r%2))] = index
				index += 1
		for w in self.white:
			hArray[posMap[w]] = 1
		for b in self.black:
			hArray[posMap[b]] = 2
		return int(self.h_encode(hArray, self.cols // 2, self.cols // 2))
		
	def h_encode(self, arr, w, b):
		"""
		Recursive method that uses Dan Garcia's combinatorially optimal hash.
		
		Outputs:
			Integer hash of array with two types of marks
		"""
		l = len(arr)
		if arr.count(arr[0]) == l: # All are same element
			return 0
		if arr[0] == 0:
			return self.h_encode(arr[1:], w, b)
		elif arr[0] == 1:
			return self.r(l-1,w,b) + self.h_encode(arr[1:], w-1, b)
		else: # arr[0] == 2
			return self.r(l-1, w-1, b) + self.r(l-1, w, b) + self.h_encode(arr[1:], w, b-1)
			
	def r(self, s, m, n):
		"""
		Helper method for the combinatorially optimal hash 
		"""
		if m < 0 or n < 0 or s-m-n < 0:
			return 0
		return int(math.factorial(s) / math.factorial(s-m-n)\
		/ math.factorial(m) / math.factorial(n))
		
	def generateSolutions(self, **kwargs):
		"""Returns a Iterable of Puzzle objects that are solved states

        Outputs:
            Iterable of Puzzles
        """
		newPuzzle = Bishop(bishops= self.cols // 2, rows = self.rows)
		newPuzzle.white = [(0, 2*i) for i in range(self.cols // 2)]
		newPuzzle.black = [(self.rows - 1, 2*i + 1 - (self.rows % 2)) for i in range(self.cols // 2)]
		return [newPuzzle]
		
	def serialize(self, **kwargs):
		"""Returns a serialized based on self

        Outputs:
            String Puzzle
        """
		result = []
		conv = lambda num: chr(num + 97)
		white_temp = [conv(w[1]) + str(self.rows - w[0]) for w in self.white]
		white_temp.sort(key = lambda s: s[1] + s[0])
		black_temp = [conv(b[1]) + str(self.rows - b[0]) for b in self.black]
		black_temp.sort(key = lambda s: s[1] + s[0])
		result.append(str(self.cols // 2))
		result.append(str(self.rows))
		result.append("-".join(str(x) for x in white_temp))
		result.append("-".join(str(x) for x in black_temp))
		return "_".join(result)
		
	@classmethod
	def deserialize(cls, positionid, **kwargs):
		"""Returns a Puzzle object based on positionid

        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
		puzzle = Bishop()
		deconv = lambda cha: ord(cha) - 97
		data = positionid.split("_")
		puzzle.cols = int(data[0]) * 2
		puzzle.rows = int(data[1])
		puzzle.white = []
		puzzle.black = []
		if data[2] != "":
			for string in data[2].split("-"):
				next_white = (puzzle.rows - int(string[1]), deconv(string[0]))
				puzzle.white.append(next_white)
		if data[3] != "":
			for string in data[3].split("-"):
				next_black = (puzzle.rows - int(string[1]), deconv(string[0]))
				puzzle.black.append(next_black)
		return puzzle
		
	@classmethod
	def isLegalPosition(cls, positionid, variantid=None, **kwargs):
		"""Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified

        Outputs:
            - True if Puzzle is valid, else False
        """
		try: puzzle = cls.deserialize(positionid)
		except: return False
		unique = set()
		w_sum, w_diff = set(), set()
		if len(puzzle.white) != puzzle.cols // 2: return False
		if len(puzzle.black) != puzzle.cols // 2: return False
		for w in puzzle.white:
			if w[0] < 0 or w[1] < 0 or w[0] >= puzzle.rows or w[1] >= puzzle.cols \
			or (w[0] + w[1]) % 2 == 1: # Proven by diagonal property
				return False
			if w in unique:
				return False
			unique.add(w)
			w_sum.add(w[0] + w[1])
			w_diff.add(w[0] - w[1])
		for b in puzzle.black:
			if b[0] < 0 or b[1] < 0 or b[0] >= puzzle.rows or b[1] >= puzzle.cols \
			or (b[0] + b[1]) % 2 == 1:
				return False
			if b in unique or b[0] + b[1] in w_sum or b[0] - b[1] in w_diff:
				return False
			unique.add(b)
		return True
		
	@classmethod
	def generateStartPosition(cls, variantid, **kwargs):
		"""Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
		if not isinstance(variantid, str): raise TypeError("Invalid variantid")
		if variantid not in Bishop.variants: raise IndexError("Out of bounds variantid")
		return Bishop(bishops = int(variantid[0]), rows = int(variantid[2]))

