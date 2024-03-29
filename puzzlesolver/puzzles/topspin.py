"""
File: topspin.py
Puzzle: Top Spin
Author: Yishu Chao
Date: November 23, 2020
"""

from . import ServerPuzzle
from ..util import *
from ..solvers import SqliteSolver
import math
import random

class TopSpin(ServerPuzzle):

	id = 'topspin'
	variants = ['6_2']
	startRandomized = True

	def __init__(self, size = 6, spin = 2, **kwargs):
		self.size = size
		self.spin = spin
		self.all_nums = list(range(1, size+1))
		if len(kwargs) == 1:
			for key, value in kwargs.items():
				if key == 'loop':
					self.loop = value
		else:
			self.loop = random.sample(self.all_nums,size)
		self.track = [self.loop[:spin]] + [item for item in self.loop[spin:]]

	def __str__(self, **kwargs):
		return str(self.track)

	def printInfo(self):
		print("Puzzle: ")
		print('                           ')
		print ("     "+str(self.track[0]) + '\n')
		print (str(self.track[4]) + "               " + str(self.track[1]) + '\n')
		print("     " + str(self.track[3]) + "     " + str(self.track[2]))
		print('                           ')

	def primitive(self,**kwargs):
		'''
		since the track is circular, you can find where the 1 is and wrap it around
		to see if it is in sorted order
		'''
		if self.loop == self.all_nums:
			return PuzzleValue.SOLVABLE
		return PuzzleValue.UNDECIDED

	def generateMoves(self,movetype = 'all', **kwargs):
		if movetype == 'for' or movetype == 'back':
			return []
		moves = []
		for i in range(1,self.size):
			moves.append((i,'clockwise'))
		moves.append(('flip'))
		return moves

	#helper fucntion for doMove()
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
		new_puzzle = TopSpin(loop = new_loop)
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
		temp = self.all_nums
		solutions.append(TopSpin(loop = temp))
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
		temp = variantid.split('_')
		return TopSpin(size=int(temp[0]), spin = int(temp[1]))

	def toString(self, **kwargs):
		result = '_'.join([str(item) for item in self.track[0]])
		for item in self.track[1:]:
			result += '-'
			result += str(item)
		return result

	@classmethod
	def fromString(cls, variant_id, positionid):
		new_loop = []
		stacks = positionid.split('-')
		in_spin = stacks[0].split('_')
		for string in in_spin:
			new_loop.append(int(string))
		for item in stacks[1:]:
			new_loop.append(int(item))
		puzzle = TopSpin(loop=new_loop)
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
