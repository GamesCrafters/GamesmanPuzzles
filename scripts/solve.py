from puzzlesolver.puzzles import PuzzleManager

# Initalizes the data
def init_data():
    for p_cls in PuzzleManager.getPuzzleClasses():        
        if data["TESTING"]:
            variants = p_cls.test_variants
        else:
            variants = p_cls.variants
        print(p_cls, p_cls.variants)

        for variant in variants:
            s_cls = PuzzleManager.getSolverClass(p_cls.id, variant)
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=data['DATABASE_DIR'])
            solver.solve(verbose=True)


if __name__ == "__main__":
    import json

    with open("config.json") as json_data_file:
        data = json.load(json_data_file)

    init_data()