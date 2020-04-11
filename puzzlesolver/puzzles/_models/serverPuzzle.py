from ...util import *
from . import Puzzle
from abc import abstractproperty, abstractclassmethod, abstractmethod

class ServerPuzzle(Puzzle):
    
    # Methods and attributes for Server
    # Descriptions
    puzzleid = Exception("No puzzleid defined")
    author = "N/A"
    puzzle_name = "N/A"
    description = "N/A"
    date_created = "N/A"
        
    """A dictionary with the following
    - variantId as the string key
    - A Solver class object as the value

    This dictionary is meant to store Solvers for the web server to interact with.
    See Hanoi for a dict comprehension example
    """
    variants = {}

    @abstractproperty
    def variant(self):
        """Returns a string defining the variant of this puzzleself.

        Example: '5x5', '3x4', 'reverse3x3'
        """
        raise NotImplementedError
    
    @abstractclassmethod
    def deserialize(cls, positionid, **kwargs):
        """Returns a Puzzle object based on positionid

        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        raise NotImplementedError

    def serialize(self, **kwargs):
        """Returns a serialized based on self

        Outputs:
            String Puzzle
        """
        return str(self)
    
    @abstractmethod
    def isLegalPosition(self):
        """Checks if the Puzzle is valid given the rules.
        For example, Hanoi cannot have a larger ring on top of a smaller one.

        Outputs:
            - True if Puzzle is valid, else False
        """
        raise NotImplementedError 

    @abstractclassmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        raise NotImplementedError

    # Built-in functions
    @classmethod
    def validate(cls, positionid=None, variantid=None, **kwargs):
        """Checks if the positionid fits the rules set for the puzzle, as
        well as fits the variantid as well
        
        Inputs:
            - positionid: 
            - variantid: 
        """
        if variantid is not None:
            if not isinstance(variantid, str): raise PuzzleException("Invalid variantid")
            if variantid not in cls.variants: raise PuzzleException("Out of bounds variantid")
        if positionid is not None:
            try: p = cls.deserialize(positionid)
            except Exception as e: raise PuzzleException("position is not a valid puzzle") 
            if variantid is not None and p.variant != variantid: 
                raise PuzzleException("variantid doesn't match puzzleid")
            if not p.isLegalPosition(): raise PuzzleException("position is not a valid puzzle")

    def getName(self, **kwargs):
        """Returns the name of the Puzzle.

        Outputs:
            String name
        """
        return self.__class__.__name__ + self.variant
