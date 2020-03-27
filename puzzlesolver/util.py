class PuzzleValue:
    SOLVABLE = "SOLVABLE"
    UNSOLVABLE = "UNSOLVABLE"
    UNDECIDED = "UNDECIDED"

    @staticmethod
    def contains(key):
        return (key == PuzzleValue.SOLVABLE or 
                key == PuzzleValue.UNSOLVABLE or 
                key == PuzzleValue.UNDECIDED)

class PuzzleException(Exception):
    """An Exception meant to be caught by the server"""
    pass