"""
This class provides a TUI for interaction with Solvers and Puzzles
"""
from .util import PuzzleValue

class PuzzlePlayer:

    def __init__(self, puzzle, solver=None, info=True, auto=False):
        self.base = puzzle
        self.puzzle = puzzle
        self.solver = solver
        self.info = info
        if not solver and (auto or info):
            raise Exception("Cannot have auto or info arguments without a solver")
        self.auto = auto
        if solver:
            self.solver.solve(verbose=True)

    # Starts the PuzzlePlayer
    def play(self):
        self.puzzle = self.base
        self.turn = 0
        while self.puzzle.primitive() == PuzzleValue.UNDECIDED:
            self.printInfo()
            self.puzzle.printInfo()
            self.printTurn()
        self.printInfo()
        self.puzzle.printInfo()
        print("Game Over")

    def printInfo(self):
        print("Turn:          ", self.turn), 
        print("Primitive:     ", self.puzzle.primitive())
        if self.info and self.solver:
            print("Solver:        ", self.solver.getValue(self.puzzle))
            print("Remoteness:    ", self.solver.getRemoteness(self.puzzle)) 
            print("Best Move:     ", self.generateBestMove())
        self.turn += 1

    # Prompts for input and moves
    def printTurn(self):
        if self.solver: move = self.generateBestMove() 
        # Auto generate a possible solution
        if self.auto:
            self.puzzle = self.puzzle.doMove(move)
        else:
            moves = list(self.puzzle.generateMoves(movetype="legal"))
            # Have the best move be the first index
            if self.solver and self.info: 
                moves.remove(move)
                moves.insert(0, move)
            print("Possible Moves:")
            for count, m in enumerate(moves):
                print(str(count) + " -> " + str(m))
            print("Enter Piece: ")
            index = int(input())
            if index >= len(moves):
                print("Not a valid move, try again")
            else:
                self.puzzle = self.puzzle.doMove(moves[index])
        print("----------------------------")

    # Generates best move from the solver
    def generateBestMove(self):
        if self.solver.getValue(self.puzzle) == PuzzleValue.UNSOLVABLE: return None
        if self.puzzle.primitive() == PuzzleValue.SOLVABLE: return None
        remotes = {
            self.solver.getRemoteness(self.puzzle.doMove(move)) : move 
            for move in self.puzzle.generateMoves(movetype="legal")
        }
        if PuzzleValue.UNSOLVABLE in remotes:
            del remotes[PuzzleValue.UNSOLVABLE]
        return remotes[min(remotes.keys())]

if __name__ == "__main__":
    import argparse
    from puzzlesolver.puzzles import puzzleList

    parser = argparse.ArgumentParser()
    parser.add_argument("puzzleid", help="PuzzleID of the puzzle you wish to view")
    parser.add_argument("-v", "--variant", help="Variant of puzzle")
    parser.add_argument("-p", "--position", help="Specific position of puzzle (overrides variant)")
    parser.add_argument("-i", "--info", action="store_true", help="Solver reveals some helpful info")
    parser.add_argument("-a", "--auto", action="store_true", help="Puzzle plays itself")
    parser.add_argument("-l", "--list", action="store_true", help="Lists puzzles and their ids")

    args = parser.parse_args()

    if args.puzzleid not in puzzleList:
        print("Possible puzzles:")
        print("\n".join(puzzleList.keys()))
        raise Exception("Puzzleid is not recorded in PuzzleList")

    p_cls = puzzleList[args.puzzleid]

    puzzle = None    
    if args.variant:
        puzzle = p_cls.generateStartPosition(args.variant)
    if args.position:
        puzzle = p_cls.validate(args.position)
        puzzle = p_cls.deserialize(args.position)
    if not puzzle:
        puzzle = p_cls()
    
    if args.info or args.auto:
        s_cls = p_cls.variants[puzzle.variant]
        solver = s_cls(puzzle)
    else:
        solver = None

    PuzzlePlayer(puzzle, solver=solver, info=args.info, auto=args.auto).play()
