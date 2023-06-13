def get_gui_status(puzzle_id, variant_id=None):
    if puzzle_id in ('npuzzle', 'lights', 'nqueens'):
        return 'v1'
    elif puzzle_id in ('hanoi', 'rushhour'):
        return 'v2'
    else:
        return 'v0'