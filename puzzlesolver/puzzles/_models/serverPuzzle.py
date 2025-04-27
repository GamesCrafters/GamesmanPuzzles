from ...util import classproperty, deprecated
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
    def fromString(cls, variant_id, position_str):
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
            if not isinstance(position_str, str): 
                raise TypeError("PositionID must be type str")
            if not cls.isLegalPosition(position_str): 
                raise ValueError("PositionID could not be translated into a puzzle")
        raise NotImplementedError
    
    #################################################################
    # Deprecated Methods
    #################################################################

    @classmethod
    def fromHash(cls, variantid, hash_val):
        """Returns a Puzzle object based on variantid and the given hash_val
        """
        raise NotImplementedError

    @classmethod
    @deprecated("isLegalPosition is deprecated")
    def isLegalPosition(cls, positionid, variantid=None):
        """Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified
        For example, Hanoi cannot have a larger ring on top of a smaller one.

        Outputs:
            - True if Puzzle is valid, else False
        """
        raise NotImplementedError
