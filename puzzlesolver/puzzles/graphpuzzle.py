"""This puzzle is meant for testing purposes"""

from .puzzle import Puzzle
from ..util import *

class GraphPuzzle(Puzzle):

    solutions = {}
    unique_names = {}

    def __init__(self, 
                name=None,
                variantid=0,
                primitive=PuzzleValue.UNDECIDED,
                biChildren=[],
                forwardChildren=[],
                undoChildren=[],
                **kwargs):
        self.name = name
        self.variantid = variantid
        self.value = primitive
        self.biChildren = set() 
        self.forwardChildren = set()
        self.undoChildren = set()
        
        if variantid not in GraphPuzzle.unique_names: GraphPuzzle.unique_names[variantid] = set()
        if variantid not in GraphPuzzle.solutions: GraphPuzzle.solutions[variantid] = set()

        if self.name == None: raise ValueError("Name cannot be None")
        if self.name in GraphPuzzle.unique_names[variantid]: 
            raise ValueError("{} already exists: {}".format(self.name, GraphPuzzle.unique_names[variantid]))

        GraphPuzzle.unique_names[variantid].add(self.name)
        if primitive == PuzzleValue.SOLVABLE: GraphPuzzle.solutions[variantid].add(self)
        
        for child in biChildren:
            self.addBiMove(child)
        for child in forwardChildren:
            self.addForwardMove(child)
        for child in undoChildren:
            self.addUndoMove(child)

    def __hash__(self):
        return hash(str(self.name))

    def __str__(self):
        return "Puzzle: {}".format(self.name)

    def primitive(self, **kwargs):
        return self.value

    def doMove(self, move, **kwargs):
        child = move[0]
        if child == "b": index = self.biChildren
        elif child == "f": index = self.forwardChildren
        elif child == "u": index = self.undoChildren
        else: raise ValueError("Not a valid move")
        for i in index:
            if str(i.name) == str(move[1:]): return i 
        raise ValueError("Not a valid move")

    def generateMoves(self, movetype='all', **kwargs):
        children = {}
        if movetype == 'for' or movetype == 'legal' or movetype == 'all': children["f"] = self.forwardChildren
        if movetype == 'bi' or movetype == 'back' or movetype == 'legal' or movetype == 'all': children["b"] = self.biChildren
        if movetype == 'undo' or movetype == 'back' or movetype == 'all': children["u"] = self.undoChildren
        moves = []
        for i in children: 
            moves.extend(["{}{}".format(i, j.name) for j in children[i]])
        return moves

    def generateSolutions(self, **kwargs):
        return GraphPuzzle.solutions[self.variantid]
    
    def addForwardMove(self, puzzle):
        if puzzle in self.undoChildren or self in puzzle.forwardChildren or\
            self in puzzle.biChildren or puzzle in self.biChildren:
            raise ValueError("Contradictory move")
        if self.variantid != puzzle.variantid: raise ValueError("Variants must be the same")
        self.forwardChildren.add(puzzle)
        puzzle.undoChildren.add(self)
    
    def addUndoMove(self, puzzle):
        if puzzle in self.forwardChildren or self in puzzle.undoChildren or\
            self in puzzle.biChildren or puzzle in self.biChildren:
            raise ValueError("Contradictory move")
        if self.variantid != puzzle.variantid: raise ValueError("Variants must be the same")
        self.undoChildren.add(puzzle)
        puzzle.forwardChildren.add(self)
    
    def addBiMove(self, puzzle):
        if puzzle in self.forwardChildren or self in puzzle.forwardChildren or\
            self in puzzle.undoChildren or puzzle in self.undoChildren:
            raise ValueError("Contradictory move")
        if self.variantid != puzzle.variantid: raise ValueError("Variants must be the same")
        self.biChildren.add(puzzle)
        puzzle.biChildren.add(self)
    
    def removeMove(self, puzzle):
        def remove(t, e):
            try: t.remove(e)
            except: pass
        remove(self.forwardChildren, puzzle)
        remove(self.biChildren, puzzle)
        remove(self.undoChildren, puzzle)
        remove(puzzle.forwardChildren, self)
        remove(puzzle.biChildren, self)
        remove(puzzle.undoChildren, self)
    
    @staticmethod
    def variant_test(func):
        def helper():
            try: func()
            finally: 
                GraphPuzzle.solutions = {}
                GraphPuzzle.unique_names = {}
        return helper
