"""
File: bishop.py
Puzzle: Bishop Puzzle
Author: Brian Delaney (Backend), Cameron Cheung (Backend, AutoGUI)
Date: October 30, 2020
"""

from . import ServerPuzzle
from ..util import *
import math

variant_start = {
	"4x5_8": "XXXX" + "-" * 12 + "OOOO",
	"4x7_4": "X-X-" + "-" * 20 + "O-O-",
	"6x7_6": "X-X-X-" + "-" * 30 + "O-O-O-"
}

size_to_variant = {20: "4x5_8", 28: "4x7_4", 42: "6x7_6"}

components = {
	"4x5_8": ([0,2,5,7,8,10,13,15,16,18], [1,3,4,6,9,11,12,14,17,19]),
	"4x7_4": [0,2,5,7,8,10,13,15,16,18,21,23,24,26],
	"6x7_6": [0,2,4,7,9,11,12,14,16,19,21,23,24,26,28,31,33,35,36,38,40]
}

class Bishop(ServerPuzzle):
	id = 'bishoppuzzle'
	variants = ["4x5_8", "4x7_4", "6x7_6"]
	startRandomized = False

	# Indices will be in COLUMN-MAJOR order
	
	def __init__(self, variant_id, board=None):
		self.variant_id = variant_id
		self.rows = int(variant_id[0])
		self.cols = int(variant_id[2])
		self.num_bishops = int(variant_id[4])
		if board:
			self.board = board
		elif variant_id in variant_start:
			self.board = variant_start[variant_id]
		else:
			self.board = variant_start["4x5_8"]
	
	def __str__(self, **kwargs):
		return str(self.board)
	
	@property
	def variant(self):
		return self.variant_id
	
	def primitive(self, **kwargs):
		if self.board == self.generateSolutions()[0].board:
			return PuzzleValue.SOLVABLE
		return PuzzleValue.UNDECIDED
	
	def generateMoves(self, movetype='bi'):
		if movetype == 'for':
			return []
		
		prod = self.rows * self.cols
		rm1 = self.rows - 1
		all_moves = []

		attacked_by = [False, False] # [attacked by white, attacked by black]
		white_moves_to_curr_dest, black_moves_to_curr_dest = [], []
		
		def diagonal_check(dest, update, within_bounds):
			src = dest + update
			while within_bounds(src):
				if self.board[src] == 'X':
					white_moves_to_curr_dest.append((src, dest))
					attacked_by[0] = True
					break
				elif self.board[src] == 'O':
					black_moves_to_curr_dest.append((src, dest))
					attacked_by[1] = True
					break
				src += update

		for dest in range(self.rows * self.cols):
			attacked_by[0] = False
			attacked_by[1] = False
			white_moves_to_curr_dest, black_moves_to_curr_dest = [], []
			if self.board[dest] == '-':
				diagonal_check(dest, -self.rows - 1, lambda src: src >= 0 and src % self.rows != rm1) #topleft
				diagonal_check(dest, self.rows - 1, lambda src: src < prod and src % self.rows != rm1) #topright
				diagonal_check(dest, 1 - self.rows, lambda src: src >= 0 and src % self.rows != 0) #bottomleft
				diagonal_check(dest, self.rows + 1, lambda src: src < prod and src % self.rows != 0) #bottomright

				if not attacked_by[0]:
					all_moves += black_moves_to_curr_dest
				if not attacked_by[1]:
					all_moves += white_moves_to_curr_dest

		return all_moves
	
	def doMove(self, move, **kwargs):
		newBoardAsList = list(self.board)
		newBoardAsList[move[1]] = newBoardAsList[move[0]]
		newBoardAsList[move[0]] = '-'
		return Bishop(self.variant_id, ''.join(newBoardAsList))
	
	def num_rearrangements(num_slots, num_X, num_O):
		if num_slots < 0 or num_X < 0 or num_O < 0 or num_slots < num_X + num_O:
			return 0
		return math.factorial(num_slots) // (math.factorial(num_X) * math.factorial(num_O) * math.factorial(num_slots - num_X - num_O))
	
	def h(component_size, num_bishops_of_each_color_in_component, component):
		num_X = num_bishops_of_each_color_in_component
		num_O = num_bishops_of_each_color_in_component
		num_slots = component_size
		total = 0
		for piece in component:
			threshold1 = Bishop.num_rearrangements(num_slots - 1, num_X, num_O)
			threshold2 = threshold1 + Bishop.num_rearrangements(num_slots - 1, num_X, num_O - 1)
			if piece == 'O':
				total += threshold1
				num_O -= 1
			elif piece == 'X':
				total += threshold2
				num_X -= 1
			num_slots -= 1
		return total
	
	def __hash__(self):
		component_size = self.rows // 2 * self.cols
		if self.variant_id == "4x5_8":
			c1_idxs, c2_idxs = components["4x5_8"]
			component1 = [self.board[c1_idxs[i]] for i in range(component_size)]
			component2 = [self.board[c2_idxs[i]] for i in range(component_size)]
			h1 = Bishop.h(component_size, 2, component1)
			h2 = Bishop.h(component_size, 2, component2)
			return h2 * Bishop.num_rearrangements(component_size, 2, 2) + h1
		else:
			c_idxs = components[self.variant_id]
			component = [self.board[c_idxs[i]] for i in range(component_size)]
			return Bishop.h(component_size, self.num_bishops // 2, component)
	
	def generateSolutions(self, **kwargs):
		replace = lambda c: 'X' if c == 'O' else 'O' if c == 'X' else '-'
		return [Bishop(self.variant_id, ''.join([replace(c) for c in variant_start[self.variant_id]]))]
	
	@classmethod
	def fromHash(cls, variant_id, hash_val):
		""" 
		Note that this function does not actually unhash the given hash value
		because the hash method we used here is irreversible. Since this
		method is only used to generate random positions of a puzzle, we
		instead return a position that is already randomized by the constructor
		of a Rubiks instance.
		"""
		return cls(variant_id)
	
	@classmethod
	def fromString(cls, variant_id, position_str):
		"""Returns a Puzzle object based on positionid
		Inputs:
			positionid - String id from puzzle
		Outputs:
			Puzzle object based on puzzleid and variantid
		"""
		return cls(variant_id, position_str)

	def toString(self, mode):
		"""Human-readable string shall match autogui string."""
		prefix = '1_' if mode == StringMode.AUTOGUI else ''
		return prefix + self.board
    
	def moveString(self, move, mode):
		if mode == StringMode.AUTOGUI:
			return f'M_{move[0]}_{move[1]}_x'
		else:
			return f"{chr(ord('a') + self.rows - 1 - move[0] % self.rows)}{move[0] // self.rows} {chr(ord('a') + self.rows - move[1] % self.rows)}{move[1] // self.rows}"

	@classmethod
	def isLegalPosition(cls, positionid, variantid=None, **kwargs):
		"""Checks if the positionid is valid given the rules of the Puzzle cls. 
		This function is invariant and only checks if all the rules are satisified
		Outputs:
			- True if Puzzle is valid, else False
		"""
		return True

	@classmethod
	def generateStartPosition(cls, variant_id, **kwargs):
		"""Returns a Puzzle object containing the start position."""
		return Bishop(variant_id)