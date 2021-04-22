from . import GeneralSolver

import queue as q


class MPISolver(GeneralSolver):
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
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        self.rank = comm.Get_rank()
        self.size = comm.Get_size()

        # if self.rank == 0:
        #     from puzzlesolver.puzzles import Puzzle

        #     if not isinstance(puzzle, Puzzle):
        #         raise TypeError("Not a Puzzle instance")

        #     self._remoteness = {}
        #     self._queue = q.Queue()
        #     self.puzzle = puzzle

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
        # if self.rank == 0:
        #     if not isinstance(self._queue, q.Queue):
        #         self._queue = q.Queue()

        #     # BFS for remoteness classification
        #     while not self._queue.empty():
        #         puzzle = self._queue.get()
        #         for move in puzzle.generateMoves('undo'):
        #             nextPuzzle = puzzle.doMove(move)

        #             if hash(nextPuzzle) not in self._remoteness:
        #                 self._remoteness[hash(
        #                     nextPuzzle)] = self._remoteness[hash(puzzle)] + 1
        #                 self._queue.put(nextPuzzle)
