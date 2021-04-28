from .solver import Solver

from ..util import PuzzleValue, PuzzleException
import queue as q
import progressbar

class GeneralSolver(Solver):
    def __init__(self, puzzle):
        """Generates a GeneralSolver instance

        Parameters
        ----------
        puzzle : Puzzle
            The Puzzle instance you wish to solve

        Raises
        ------
        TypeError
            When puzzle is not a Puzzle
        """
        from puzzlesolver.puzzles import Puzzle

        if not isinstance(puzzle, Puzzle): 
            raise TypeError("Not a Puzzle instance")
        
        self._remoteness = {}
        self._queue = q.Queue()
        self.puzzle = puzzle
    
    def getRemoteness(self, puzzle):
        """Queries a Python dict to find the remoteness of a
        Puzzle instance.

        Parameters
        ----------
        puzzle : Puzzle
            The Puzzle instance you wish to get the Remoteness

        Returns
        -------
        Integer
            The remoteness of the Puzzle instance

        Raises
        ------
        SystemError
            If the puzzle has not been solved yet, as defined by solver.solved,
            then this Error is raised
        
        TypeError
            If the puzzle argument is not a Puzzle instance
        """
        from puzzlesolver.puzzles import Puzzle

        if not isinstance(puzzle, Puzzle):
            raise TypeError("Not a Puzzle instance")

        if not self.solved:
            raise SystemError("Solver has not been solved yet")
        if hash(puzzle) in self._remoteness: 
            return self._remoteness[hash(puzzle)]
        return PuzzleValue.MAX_REMOTENESS

    def solve(self, verbose=False):
        """Solves the puzzle inputted into the solver during initialization.

        TODO: Be able to handle interrupts, so that when even if a solver is
        interrupted during solving, as long as its in memory, it is able to continue
        solving the rest of the positions with no errors.

        Parameters
        ----------
        verbose : bool, optional
            Displays a neat little progressbar during solving.
            Maxlength is based on puzzle.numPositions if defined, by default False
        """
        if not isinstance(self._queue, q.Queue):
            self._queue = q.Queue()

        if self._queue.empty():
            solutions = self.puzzle.generateSolutions()
            if len(list(solutions)) == 0:
                # CSP - the position generated by the __init__ method is starting position
                self._cspGenerateSolutions(self._queue, verbose)
            else:
                # Not a CSP - use generateSolutions()
                for solution in solutions: 
                    # Check if all the solutions are SOLVABLE
                    assert solution.primitive() == PuzzleValue.SOLVABLE, "`generateSolutions` contains an UNSOLVABLE position"
                    self._remoteness[hash(solution)] = 0
                    self._queue.put(solution)
                
        # Progressbar
        if verbose: 
            print('Solving: {}{}'.format(self.puzzle.name, self.puzzle.variant))
            bar = progressbar.ProgressBar(max_value=self.puzzle.numPositions)

        # BFS for remoteness classification                        
        while not self._queue.empty():
            if verbose: bar.update(len(self._remoteness))
            puzzle = self._queue.get()
            for move in puzzle.generateMoves('undo'):
                nextPuzzle = puzzle.doMove(move)

                if hash(nextPuzzle) not in self._remoteness:
                    assert nextPuzzle.primitive() != PuzzleValue.SOLVABLE, """
                        Found a state where primitive was SOLVABLE while traversing Puzzle tree
                    """
                    self._remoteness[hash(nextPuzzle)] = self._remoteness[hash(puzzle)] + 1
                    self._queue.put(nextPuzzle)
        if verbose: bar.finish()

    @property
    def solved(self):
        """A condition that checks if the Solver is solved. This is True
        when the remoteness dictionary is not empty or the queue is not empty.

        Returns
        -------
        Condition
            Returns if the Solver finished solving
        """
        return self._remoteness and self._queue.empty()

    def _cspGenerateSolutions(self, queue, verbose=False):
        """
        Traverse the puzzle tree, starting from the position returned from __init__,
        placing primitive positions found in queue.
        """
        # Progressbar
        if verbose:
            print("Finding primitive positions: {}{}".format(self.puzzle.name, self.puzzle.variant))
            bar = progressbar.ProgressBar(max_value=self.puzzle.numPositions)
            
        queue_2, found = q.Queue(), set()
        queue_2.put(self.puzzle)
        found.add(hash(self.puzzle))
        
        # BFS search for primitive positions
        # TODO (maybe not?): Make this only require one search
        i = 1
        while not queue_2.empty():
            if verbose: bar.update(i)
            puzzle = queue_2.get()
            if puzzle.primitive() == PuzzleValue.SOLVABLE:
                self._remoteness[hash(puzzle)] = 0
                queue.put(puzzle)
            for move in puzzle.generateMoves('legal'):
                nextPuzzle = puzzle.doMove(move)
                if hash(nextPuzzle) not in found:
                    found.add(hash(nextPuzzle))
                    queue_2.put(nextPuzzle)
            i += 1
        if verbose: bar.finish()
