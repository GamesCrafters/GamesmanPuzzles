def get_gui_status(puzzle_id, variant_id=None):
    if puzzle_id in ('lights', 'nqueens'):
        return 'v1'
    elif puzzle_id in ('hanoi', 'rushhour', 'npuzzle'):
        return 'v2'
    else:
        return 'v0'