from .puzzles import *
from .solver import *

def variantWrapper(puzzle_class, variant_id, *args, **kwargs):
    def puzzleWrapper(position_id, variant_id):
        if position_id and not puzzle_class.checkValidVariant(position_id, variant_id):
            raise ValueError     
        return puzzle_class(*args, **kwargs, position_id=position_id, variant_id=variant_id)
    return lambda position_id=None : puzzleWrapper(position_id, variant_id)

puzzleList = {
    'hanoi' : {
        'name': 'Hanoi',
        'variants': {
            str(i): {
                'desc': 'A puzzle based on the Towers of Hanoi',
                'solver': PickleSolverWrapper,
                'puzzle': variantWrapper(Hanoi, i)
            } for i in range(1,11)
        }
    },
}