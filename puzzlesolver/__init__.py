from .puzzles import *
from .solver import *

puzzleList = {
    'hanoi' :
    {
        'name': 'Hanoi',
        'desc': 'A puzzle based on the Towers of Hanoi',
        'solver': solver.PickleSolverWrapper,
        'puzzle': puzzles.Hanoi
    }
}