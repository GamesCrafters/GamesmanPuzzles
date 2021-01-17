"""This puzzle is meant for testing purposes"""

from . import Puzzle
from ..util import *
import networkx as nx

class GraphPuzzle(Puzzle):

    def __init__(self, name,
                value=PuzzleValue.UNDECIDED,
                csp=False,
                **kwargs):
        if name == None: raise ValueError("Name cannot be None")
        if not PuzzleValue.contains(value): raise ValueError("Not a valid value")
        self.name = name
        self.value = value
        self.csp = csp

        self.graph = nx.DiGraph()
        self.graph.add_node(self.name, value=value, obj=self)
        self.solutions = set([self]) if value == PuzzleValue.SOLVABLE else set()

    def _addChild(self, child, value=None):
        if isinstance(child, GraphPuzzle):
            if self.graph != child.graph:
                if child.name == self.name: raise ValueError("Cannot have move to self")
                intersection = set(child.graph) & set(self.graph)
                for node in intersection:
                    if child.graph.nodes[node] != self.graph.nodes[node]:
                        raise ValueError("Contradictory values on node {}".format(node))
                if nx.symmetric_difference(child.graph.subgraph(intersection), 
                    self.graph.subgraph(intersection)):
                    raise ValueError("Intersection between graphs contain contradictory edges")
                self.graph.update(child.graph)
                self.solutions.update(child.solutions)
                for node in self.graph:
                    if 'obj' in self.graph.nodes[node]:
                        puzzle = self.graph.nodes[node]['obj']
                        puzzle.graph = self.graph
                        puzzle.solutions = self.solutions
            value = child.value
            child = child.name
        self.graph.nodes[child]['value'] = value
        return child
        
    def __hash__(self):
        return hash(str(self.name))

    def __eq__(self, puzzle):
        return (isinstance(puzzle, GraphPuzzle) and 
                self.name == puzzle.name and
                self.value == puzzle.value and
                self.graph == puzzle.graph and
                self.solutions == puzzle.solutions)

    def __str__(self):
        return "Puzzle: {}".format(self.name)

    def primitive(self, **kwargs):
        return self.value

    def doMove(self, move, **kwargs):
        if move not in self.generateMoves(): raise ValueError("Not a valid move")
        if 'obj' in self.graph.nodes[move]: return self.graph.nodes[move]['obj']
        newPuzzle = GraphPuzzle(move, self.graph.nodes[move]['value'], self.csp)
        newPuzzle.solutions = self.solutions
        newPuzzle.graph = self.graph
        self.graph.nodes[move]['obj'] = newPuzzle
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
        if self.csp: return []
        else: return self.solutions
    
    def setMove(self, child, movetype="for"):
        child = self._addChild(child)
        if self.name == child: raise ValueError("Cannot make move to same state")
        self.removeMove(child)
        if movetype == "bi":
            self.graph.add_edge(self.name, child)
            self.graph.add_edge(child, self.name)
        if movetype == "for":
            self.graph.add_edge(self.name, child)
        if movetype == "back":
            self.graph.add_edge(child, self.name)

    def removeMove(self, child):
        if isinstance(child, GraphPuzzle):
            child = child.name
        self.graph.remove_edges_from([(self.name, child), (child, self.name)])

    def connected(self, child):
        if not isinstance(child, GraphPuzzle):
            raise ValueError("Not a GraphPuzzle")
        return self.graph == child.graph
