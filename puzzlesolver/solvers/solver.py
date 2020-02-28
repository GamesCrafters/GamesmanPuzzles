#These are general functions that you might want to implement if you are to use the PuzzlePlayer

class Solver:

    def solve(self, puzzle, *args, **kwargs):
        """Finds the value of the puzzle

        Inputs
        puzzle -- the puzzle in question

        Outputs:
        value of puzzle
        """
        raise NotImplementedError
    
    def getRemoteness(self, puzzle, *args, **kwargs):
        """Finds the remoteness of the puzzle

        Inputs:
        puzzle -- the puzzle in question

        Outputs:
        remoteness of puzzle
        """
        return "Not implemented :)"        