from ...util import PuzzleException, classproperty, depreciated
from . import Puzzle

class ServerPuzzle(Puzzle):
    
    #################################################################
    # Variants
    #################################################################

    @classproperty
    def variants(cls):
        """A Collections object that holds all the supported variants 
        that a Puzzle will support. 
        """ 
        return {}

    @classproperty
    def test_variants(cls):
        """
        Same as variants, except for testing purposes
        """
        return {}
    
    #################################################################
    # Deserialization
    #################################################################

    @classmethod
    def fromString(cls, positionid):
        """Returns a Puzzle object based on "minimal"
        String representation of the Puzzle (i.e. `toString(mode="minimal")`)

        Example: positionid="6-1-0" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Must raise a TypeError if the positionid is not a String
        Must raise a ValueError if the String cannot be translated into a Puzzle
        
        NOTE: A String cannot be translated into a Puzzle if it leads to an illegal
        position based on the rules of the Puzzle

        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        if hasattr(cls, "isLegalPosition"):
            if not isinstance(positionid, str): 
                raise TypeError("PositionID must be type str")
            if not cls.isLegalPosition(positionid): 
                raise ValueError("PositionID could not be translated into a puzzle")
        if hasattr(cls, "deserialize"):
            return cls.deserialize(positionid)
        raise NotImplementedError
    
    #################################################################
    # Depreciated Methods
    #################################################################

    @depreciated("serverPuzzle.serialize is depreciated. See serverPuzzle.fromString")
    def serialize(self):
        """Returns a serialized based on self

        Outputs:
            String Puzzle
        """
        return str(self)
    
    @classmethod
    @depreciated("serverPuzzle.deserialize is depreciated. See puzzle.toString")
    def deserialize(cls, positionid):
        """Returns a Puzzle object based on positionid

        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it

        Outputs:
            Puzzle object based on puzzleid and variantid
        """

        raise NotImplementedError

    @classmethod
    @depreciated("isLegalPosition is depreciated")
    def isLegalPosition(cls, positionid, variantid=None):
        """Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified
        For example, Hanoi cannot have a larger ring on top of a smaller one.

        Outputs:
            - True if Puzzle is valid, else False
        """
        raise NotImplementedError 