from ...util import *
from . import Puzzle
from dataclasses import dataclass

class ServerPuzzle(Puzzle):
    
    # Methods and attributes for Server
    """A dictionary with the following
    - variantId as the string key
    - A Solver class object as the value

    This dictionary is meant to store Solvers for the web server to interact with.
    See Hanoi for a dict comprehension example
    """
    variants = {}                

    @property
    def variant(self):
        raise NotImplementedError
    
    @dataclass
    class PuzzleDetails:
        name: str
        authors: str
        description: str
        date_added: str

    details = PuzzleDetails("Hanoi", "Anthony Ling", "A puzzle", "May 27, 2020")

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        """Returns a Puzzle object containing the start position.
        
        Outputs:
            - Puzzle object
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, puzzleid, **kwargs):
        """Returns a Puzzle object based on puzzleid

        Example: puzzleid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Inputes:
            puzzleid - String id from puzzle, serialize() must be able to generate it

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

    @classmethod
    def validate(cls, puzzleid, variantid, **kwargs):
        """Checks if the puzzleid fits the rules set for the puzzle, as
        well as fits the variantid as well
        
        Inputs:
            - puzzleid: 
            - variantid: 
        """
        if not isinstance(variantid, str): raise PuzzleException("Invalid variantid")
        if variantid not in cls.variants: raise PuzzleException("Out of bounds variantid")
        try: p = cls.deserialize(puzzleid)
        except: raise PuzzleException("puzzleid is not a valid puzzle") 
        if p.variant != variantid: raise PuzzleException("variantid doesn't match puzzleid")
        if not p.isLegalPosition(): raise PuzzleException("puzzleid is not a valid puzzle")
    
    def isLegalPostion(self):
        """Checks if the Puzzle is valid given the rules.
        For example, Hanoi cannot have a larger ring on top of a smaller one.

        Outputs:
            - True if Puzzle is valid, else False
        """
        raise NotImplementedError 