"""
This class provides a TUI for interaction with Solvers and Puzzles
"""
from puzzlesolver.util import PuzzleValue

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
        print("Turn:                  ", self.turn), 
        if self.puzzle.primitive() == 'UNDECIDED':
            prim = "UNDECIDED"
        else:
            prim = "SOLVED"
        print("Primitive:             ", prim)
        if self.info and self.solver:
            if self.solver.getValue(self.puzzle) == 'UNSOLVABLE':
                pos = "LOSE"
            else: 
                pos = "WIN"
            print("Position:              ", pos)
            print("Remoteness:            ", self.solver.getRemoteness(self.puzzle))
            best_move, remotes, unsolve = self.generateBestMove()
            self.printBestMoves(remotes, unsolve)
        self.turn += 1

    # Prompts for input and moves
    def printTurn(self):
        if self.solver: move, _, _ = self.generateBestMove() 
        # Auto generate a possible solution
        if self.auto:
            self.puzzle = self.puzzle.doMove(move)
        else:
            moves = list(self.puzzle.generateMoves(movetype="legal"))
            # Have the best move be the first index
            if len(moves) == 0:
                print("Game Over")
                exit()
            if self.solver and self.info and move: 
                moves.remove(move)
                moves.insert(0, move)
            play = self.puzzle.playPuzzle(moves)
            if play == "BEST":
                self.puzzle = self.puzzle.doMove(moves[0])
            elif play not in moves or play == "OOPS":
                print("Not a valid move, try again")
            else:
                self.puzzle = self.puzzle.doMove(play)
        print("----------------------------")

    # Generates best move from the solver
    def generateBestMove(self):
        # if self.solver.getValue(self.puzzle) == PuzzleValue.UNSOLVABLE: return None, None, None
        # if self.puzzle.primitive() == PuzzleValue.SOLVABLE: return None, None, None
        remotes = {
            str(move) : self.solver.getRemoteness(self.puzzle.doMove(move)) 
            for move in self.puzzle.generateMoves(movetype="legal")
        }
        min_remote = float('inf')
        best_move = None
        unsolve = {}
        for key, value in remotes.items():
            if value == PuzzleValue.UNSOLVABLE:
                unsolve[key] = value
            elif value < min_remote:
                min_remote = value
                best_move = key
        for key in unsolve.keys():
            del remotes[key]
        return best_move, remotes, unsolve

    def printBestMoves(self, remotes, unsolve):
        print("Winning Moves: ")
        drawing = []
        if remotes: 
            sorted_remotes = {k: v for k, v in sorted(remotes.items(), key=lambda item: item[1])}
            smallest = list(sorted_remotes.values())[0]
            for k, v in sorted_remotes.items():
                if smallest != v:
                    drawing.append((k,v))
                else:
                    space = 22 - len(k)
                    printer = " " * space
                    print("- " + str(k) + printer + str(v))
        else:
            print("- <None>")
        print("Drawing Moves: ")
        if drawing:
            for i in drawing:
                k,v = i[0], i[1]
                space = 22 - len(k)
                printer = " " * space
                print("- " + str(k) + printer + str(v))
        else:
            print("- <None>")
        print("Losing Moves: ")
        if unsolve:
            for k in unsolve.keys():
                print("- " + str(k))
        else:
            print("- <None>")

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
