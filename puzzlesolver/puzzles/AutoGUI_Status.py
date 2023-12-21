gui_status = {
    'bishop': { None: 'v3' },
    'hanoi': {
        None: 'v3',
        '5_1': 'v1',
        '5_2': 'v1',
        '5_3': 'v1',
        '5_4': 'v1',
        '4_5': 'v1',
        '4_6': 'v1',
        '3_5': 'v1',
        '3_6': 'v1',
        '3_7': 'v1',
        '3_8': 'v1'
    },
    'lights': { None: 'v3' },
    'npuzzle': { None: 'v3' },
    'nqueens': { None: 'v3' },
    'pegsolitaire': { None: 'v3' },
    'toadsandfrogspuzzle': { None: 'v3' },
    'rubiks': { None: 'v2' },
    'rushhour': { None: 'v3' }
}

def get_gui_status(puzzle_id, variant_id=None):
    if puzzle_id in gui_status:
        if variant_id in gui_status[puzzle_id]:
            return gui_status[puzzle_id][variant_id]
        else:
            return gui_status[puzzle_id][None]
    else:
        return 'v0'