from puzzlesolver.puzzles import PuzzleManager
import argparse
import json
import sys

def get_available_puzzles():
    return [p_cls.id for p_cls in PuzzleManager.getPuzzleClasses()]

def init_data(puzzle_name=None):
    for p_cls in PuzzleManager.getPuzzleClasses():
        # Skip if puzzle name is specified and doesn't match
        if puzzle_name and p_cls.id.lower() != puzzle_name.lower():
            continue
            
        if data["TESTING"]:
            variants = p_cls.test_variants
        else:
            variants = p_cls.variants
        for variant in variants:
            s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=data['DATABASE_DIR'])
            solver.solve(verbose=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solve GamesmanPuzzles')
    parser.add_argument('puzzle', nargs='?', help='Name of the puzzle to solve. If not provided, solves all puzzles.')
    parser.add_argument('--list', action='store_true', help='List all available puzzles')
    args = parser.parse_args()

    # Load configuration
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    if args.list:
        print("Available puzzles:")
        for puzzle in get_available_puzzles():
            print(f"- {puzzle}")
        sys.exit(0)

    if args.puzzle:
        available_puzzles = get_available_puzzles()
        if args.puzzle.lower() not in [p.lower() for p in available_puzzles]:
            print(f"Error: Puzzle '{args.puzzle}' not found.")
            print("\nAvailable puzzles:")
            for puzzle in available_puzzles:
                print(f"- {puzzle}")
            sys.exit(1)
        print(f"Solving puzzle: {args.puzzle}")
    
    init_data(args.puzzle)
