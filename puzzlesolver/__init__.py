from . import util
from . import solvers
from . import puzzles
from . import players

import sys

if not sys.warnoptions:
    import os, warnings
    warnings.simplefilter("default")
    os.environ["PYTHONWARNINGS"] = "default"