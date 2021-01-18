try:
    from ..._puzzlesolverc import Puzzle
    from ..._puzzlesolverc import ServerPuzzle
except (ImportError, ModuleNotFoundError):
    from .puzzle import Puzzle
    from .serverPuzzle import ServerPuzzle