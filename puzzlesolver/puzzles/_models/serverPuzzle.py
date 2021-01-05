from ...util import PuzzleException, classproperty
from . import Puzzle

class ServerPuzzle(Puzzle):
    
    #################################################################
    # Variants
    #################################################################

    @classproperty
    def variants(cls):
        """A Collections object that holds all the supported variants 
        that a Puzzle can handle. 
        
        Typically a dictionary with the following
        - variantId as the string key
        - A Solver class object as the value

        This dictionary is meant to store Solvers for the web server to interact with.
        See Hanoi for a dict comprehension example
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

        Example: positionid="3_2-1-" for Hanoi creates a Hanoi puzzle
        with two stacks of discs ((3,2) and (1))

        Must raise a TypeError if the String cannot be translated into a Puzzle

        Inputs:
            positionid - String id from puzzle, serialize() must be able to generate it

        Outputs:
            Puzzle object based on puzzleid and variantid
        """
        if (hasattr(cls, "deserialize")):
            return cls.deserialize(positionid)
        raise NotImplementedError
    
    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        """Checks if the positionid is valid given the rules of the Puzzle cls. 
        This function is invariant and only checks if all the rules are satisified
        For example, Hanoi cannot have a larger ring on top of a smaller one.

        Outputs:
            - True if Puzzle is valid, else False
        """
        raise NotImplementedError 

    @classmethod
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
        well as if it's supported by the app.
        
        Inputs:
            - positionid: 
            - variantid: 
        """
        if variantid is not None:
            if not isinstance(variantid, str): raise PuzzleException("Invalid variantid")
            if variantid not in cls.variants: raise PuzzleException("Out of bounds variantid")
        if positionid is not None:
            if not cls.isLegalPosition(positionid): raise PuzzleException("position is not a valid puzzle")
            p = cls.deserialize(positionid)
            if variantid is not None and p.variant != variantid: 
                raise PuzzleException("variantid doesn't match puzzleid")            

    @classmethod
    def getSolverClass(cls, variant=None, test=False):
        """Returns the recommended solver type, which can be based on
        variant. All recommended solvers must be persistent based.

        Outputs:
            Vary, can be Solver type or String representing solver
        """
        if test and isinstance(cls.test_variants, dict) and variant in cls.test_variants:
            return cls.test_variants[variant]
        elif not test and isinstance(cls.variants, dict) and variant in cls.variants:
            return cls.variants[variant]
        raise NotImplementedError

    def serialize(self, **kwargs):
        """Returns a serialized based on self

        Outputs:
            String Puzzle
        """
        return str(self)
    
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
