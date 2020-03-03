"""This puzzle is meant for testing purposes"""

from .puzzle import Puzzle
from ..util import *
from networkx import nx

class GraphPuzzle(Puzzle):

    def __init__(self, name,
                value=PuzzleValue.UNDECIDED,
                children={},
                **kwargs):
        self.name = name
        self.value = value

        self.graph = nx.DiGraph()
        self.graph.add_node(self.name, value=value)
        self.solutions = set([self.name]) if value == PuzzleValue.SOLVABLE else set()
        for movetype in children:
            for child in children[movetype]:
                self.setMove(child, movetype)   

    def __child(self, child):
        if isinstance(child, GraphPuzzle):
            self.graph.update(child.graph)
            self.solutions.update(child.solutions)
            child.graph = self.graph
            child.solutions = self.solutions
            child = (child.name, child.value)
        if len(child) != 2: raise ValueError("Not a valid child")
        self.graph.nodes[child[0]]['value'] = child[1]
        return child
        
    def __hash__(self):
        return hash(str(self.name))

    def __eq__(self, puzzle):
        return isinstance(puzzle, GraphPuzzle) and self.graph == puzzle.graph

    def __str__(self):
        return "Puzzle: {}".format(self.name)

    def primitive(self, **kwargs):
        return self.value

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError("Not a valid move")
        newPuzzle = GraphPuzzle(move, self.graph.nodes[move]['value'])
        newPuzzle.solutions = self.solutions
        newPuzzle.graph = self.graph
        return newPuzzle

    def generateMoves(self, movetype='all', **kwargs):
        undo = set(self.graph.reverse(False)[self.name])
        legal = set(self.graph[self.name]) 
        if movetype == 'undo': return undo
        if movetype == 'legal': return legal
        if movetype == 'bi': return undo & legal
        if movetype == 'for': return legal - (undo & legal)
        if movetype == 'back': return undo - (undo & legal)
        if movetype == 'all': return undo | legal
        raise ValueError("Invalid movetype {}".format(movetype))

    def generateSolutions(self, **kwargs):
        return self.solutions
    
    def setMove(self, child, movetype="for"):
        child = self.__child(child)
        if self.name == child[0]: raise ValueError("Cannot make move to same state")
        self.removeMove(child)
        if movetype == "bi":
            self.graph.add_edge(self.name, child[0])
            self.graph.add_edge(child[0], self.name)
        if movetype == "for":
            self.graph.add_edge(self.name, child[0])
        if movetype == "back":
            self.graph.add_edge(child[0], self.name)
        self.graph.nodes[child[0]]['value'] = child[1]

    def removeMove(self, child):
        self.graph.remove_edges_from([(self.name, child), (child, self.name)])
