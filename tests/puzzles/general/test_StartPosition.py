from puzzlesolver.puzzles import PuzzleManager

# Test the basic serialize for the start position
def test_serialize():
    output = True
    for p_cls in PuzzleManager.getPuzzleClasses():
        for variantid in p_cls.variants:
            puzzle = p_cls.generateStartPosition(variantid)
            p_str = puzzle.toString(mode="minimal")
            puzzle = p_cls.fromString(p_str)
