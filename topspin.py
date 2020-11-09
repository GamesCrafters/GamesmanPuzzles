from copy import deepcopy
from puzzlesolver.util import *
from puzzlesolver.puzzles import Puzzle
from puzzlesolver.solvers import SqliteSolver
from puzzlesolver.solvers import GeneralSolver
from puzzleplayer import PuzzlePlayer
from hashlib import sha1
import random

class TopSpin(Puzzle):

	puzzleid = 'top_spin'
	#variants = {'7' : SqliteSolver}

	def __init__(self, size = 6, **kwargs):
		self.size = size
		self.all_nums = list(range(1, size+1))
		if len(kwargs) == 1:
			self.first = False
			for key, value in kwargs.items():
				if key == 'track':
					self.track = value
					self.spin = self.track[2]
					self.loop = [
						self.track[0], 
						self.track[1], 
						self.track[2][0], 
						self.track[2][1],
						self.track[3],
						self.track[4]]
		else:
			base = random.sample(self.all_nums,size)
			self.first = True
			self.spin = base[2:4]
			self.track = [
				base[0], 
				base[1], 
				self.spin,
				base[4], 
				base[5]]
			self.loop = base

			

	def __str__(self, **kwargs):
		return str(self.track)

	def printInfo(self):
		print("Puzzle: ")
		print('                           ')
		print ("     "+str(self.track[2]) + '\n')
		print (str(self.track[1]) + "               " + str(self.track[3]) + '\n')
		print("     " + str(self.track[0]) + "     " + str(self.track[4]))
		print('                           ')


	def primitive(self,**kwargs):
		'''
		since the track is circular, you can find where the 1 is and wrap it around
		to see if it is in sorted order
		'''
		if self.loop == [5,6,1,2,3,4]:
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
		temp = [0 for _ in range(self.size)]
		if len(move) == 2:
			if move[1] == 'cntrclockwise':
				idx_change = - move[0]
			else:
				idx_change = move[0]
			for i in range(self.size):
				temp[self.handleMove(i, idx_change)] = self.loop[i]
			new_track = [temp[0],temp[1],[temp[2],temp[3]],temp[4],temp[5]]
		else:
			spin = self.track[2][::-1]
			new_track = [self.track[0],self.track[1],spin,self.track[3],self.track[4]]
		new_puzzle = TopSpin(track = new_track)
		return new_puzzle

	
	#Solver Functions
	def __hash__(self):
		h = sha1()
		h.update(str(self.loop).encode())
		return int(h.hexdigest(), 16)

	def generateSolutions(self, **kwargs):
		solutions = []
		temp = [5,6,[1,2],3,4]
		solutions.append(TopSpin(track = temp))
		return solutions
	
	'''
	@property
	def variant(self):
		size = len(self.loop)
		return str(size)


	def serialize(self, **kwargs):
		str_rep = ''
		for item in self.track:
			str_rep += str(item)
			str_rep += '-'
		return str_rep

	@classmethod
	def deserialize(cls, positionid, **kwargs):
		puzzle = TopSpin()
        puzzle.loop = []
        stacks = positionid.split("-")
        for string in stacks:
            if string != "":
                stack = [int(x) for x in string.split("_")]
                puzzle.stacks.append(stack)
            else: puzzle.stacks.append([])
        return puzzle


	@classmethod
	def generateStartPosition(cls, variantid, **kwargs):
		if not isinstance(variantid, str): raise TypeError("Invalid variantid")
		if variantid not in TopSpin.variants: raise IndexError("Out of bounds variantid")
		return TopSpin(size=int(variantid))
	'''


puzzle = TopSpin()
PuzzlePlayer(puzzle, solver=GeneralSolver(puzzle)).play()