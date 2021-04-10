from puzzlesolver.puzzles import PuzzleManager

def test_attributes():
    output = True
    for p_cls in PuzzleManager.getPuzzleClasses():
        attrs = ["id", "auth", "name", "desc", "date"]
        for a in attrs:
            if not hasattr(p_cls, a) or getattr(p_cls, a) is None: 
                print("%s doesn't have attr %s" % (p_cls.__name__, a))
                output = False
    if not output: raise Exception
                