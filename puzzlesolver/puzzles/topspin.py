"""
File: topspin.py
Puzzle: Top Spin
Author: Yishu Chao (2020) | Update: Esther Zeng, Maria Rufova, Benji Xu (2025)
Date: November 23, 2020 | Update: April 29, 2025
"""

from . import ServerPuzzle
from ..util import *
from ..solvers import SqliteSolver
import math
import random

class TopSpin(ServerPuzzle):

	id = 'topspin'
	variants = ['10_2', '12_3']
	startRandomized = True

	def __init__(self, size = 10, spin = 2, **kwargs):
		self.size = size
		self.spin = spin
		self.all_nums = list(range(1, size + 1))
		if len(kwargs) == 1:
			for key, value in kwargs.items():
				if key == 'loop':
					self.loop = value
		else:
			self.loop = random.sample(self.all_nums, size)
		self.track = [self.loop[:spin]] + [item for item in self.loop[spin:]]

	def __str__(self, **kwargs):
		return str(self.track)

	def primitive(self, **kwargs):
		'''
		since the track is circular, you can find where the 1 is and wrap it around
		to see if it is in sorted order
		'''
		if self.loop == self.all_nums:
			return PuzzleValue.SOLVABLE
		return PuzzleValue.UNDECIDED

	def generateMoves(self, movetype = 'all', **kwargs):
		if movetype == 'for' or movetype == 'back':
			return []
		moves = []
		for i in range(1, self.size):
			moves.append((i, 'clockwise'))
		moves.append(('flip'))
		return moves

	# helper fucntion for doMove()
	def handleMove(self, idx, move):
		if 0 <= idx + move <= self.size - 1:
			return idx + move
		elif idx + move < 0:
			return self.size + idx + move
		elif idx + move > self.size -1:
			return idx + move - self.size

	def doMove(self, move, **kwargs):
		if move not in self.generateMoves():
			raise ValueError
		new_loop = [0 for _ in range(self.size)]
		if len(move) == 2:
			idx_change = move[0]
			for i in range(self.size):
				new_loop[self.handleMove(i, idx_change)] = self.loop[i]
		else:
			spinned = self.loop[:self.spin][::-1]
			new_loop = spinned + self.loop[self.spin:]
		new_puzzle = TopSpin(size = self.size, spin = self.spin, loop=new_loop)
		return new_puzzle

	def __hash__(self):
		# Returns the permutation index of self.loop
		h = 0
		nums = list(range(1, self.size + 1))
		for i in range(self.size):
			j = nums.index(self.loop[i])
			del nums[j]
			h += j * math.factorial(self.size - i - 1)
		return h

	def generateSolutions(self, **kwargs):
		solutions = []
		solutions.append(TopSpin(size=self.size, spin=self.spin, loop=self.all_nums))
		return solutions

	@property
	def variant(self):
		size = str(len(self.loop))
		spin = str(len(self.track[0]))
		var = size + '_' + spin
		return var

	@classmethod
	def fromHash(cls, variantid, hash_val):
		temp = variantid.split('_')
		size = int(temp[0])
		spin = int(temp[1])
		loop = []
		nums = list(range(1, size+1))
		for i in range(size):
			numPermutation = math.factorial(size - i -1)
			loop.append(nums.pop(hash_val // numPermutation))
			hash_val %= numPermutation
		return cls(size, spin, loop=loop)

	@classmethod
	def generateStartPosition(cls, variantid, **kwargs):
		if not isinstance(variantid, str):
			raise TypeError("Invalid variantid")
		if variantid not in TopSpin.variants:
			raise IndexError("Out of bounds variantid")
		temp = variantid.split('_') # size_spin
		return TopSpin(size=int(temp[0]), spin = int(temp[1]))

	def toString(self, mode: StringMode):
		if mode == StringMode.AUTOGUI:
			# b for 10, c for 11, etc...
			return '1_a' + "".join([str(i) if i <= 9 else chr(88 + i) for i in self.track[0] + self.track[1:]])
			# return '1_a' + "".join([str(i) if i != 10 else 'i' for i in self.track[0] + self.track[1:]])

		result = '_'.join([str(item) for item in self.track[0]])
		for item in self.track[1:]:
			result += '-'
			result += str(item)
		return result

	def turncount_to_textnum(self, turn_count: int) -> int:
		"""
		returns
		"""
		flat = [i if i <= 9 else chr(88 + i) for i in self.track[0] + self.track[1:]]
		return flat[-turn_count]

	# add moveString
	def moveString(self, move, mode: StringMode):
		if mode == StringMode.AUTOGUI:
			if move == 'flip':
				return 'A_a_0_-'
			return f"A_{self.turncount_to_textnum(move[0])}_{1 + self.size - move[0]}_x"
		else:
			if move == 'flip':
				return 'flip'
			else: # example: rotate 5 steps clockwise
				return f"rotate {move[0]} step{'' if move[0] == 1 else 's'} {move[1]}"

	@classmethod
	def fromString(cls, variant_id, positionid):
		new_loop = []
		stacks = positionid.split('-')
		in_spin = stacks[0].split('_')
		for string in in_spin:
			new_loop.append(int(string))
		for item in stacks[1:]:
			new_loop.append(int(item))
		puzzle = TopSpin(size=len(new_loop), spin=len(in_spin), loop=new_loop)
		return puzzle

	@classmethod
	def isLegalPosition(cls, positionid, variantid=None, **kwargs):
		try:
			puzzle = cls.fromString(positionid)
		except:
			return False
		size = int(puzzle.variant[0])
		in_spinner = int(puzzle.variant[2])
		if len(puzzle.loop) != size:
			return False
		elif len(puzzle.track[0]) != in_spinner:
			return False
		elif max(puzzle.loop) > size or min(puzzle.loop) < 1:
			return False
		for i in range(len(puzzle.loop)):
			for j in range(i+1, len(puzzle.loop)):
				if puzzle.loop[i] == puzzle.loop[j]:
					return False
		return True
