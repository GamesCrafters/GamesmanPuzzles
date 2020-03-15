class PuzzleValue:
    SOLVABLE = "SOLVABLE"
    UNSOLVABLE = "UNSOLVABLE"
    UNDECIDED = "UNDECIDED"

class PuzzleException(Exception):
    """An Exception meant to be caught by the server"""
    pass