import pytest
import tempfile

from puzzlesolver import server
from puzzlesolver.util import PuzzleValue
from puzzlesolver.puzzles import puzzleList, GraphPuzzle

########################################################################
# Server Fixtures
########################################################################

@pytest.fixture
def client(tmpdir):
    app = server.app
    if app.config['TESTING'] != True:
        app.config['TESTING'] = True
        app.config['DATABASE_DIR'] = tmpdir

        server.init_data()

    with app.test_client() as client:
        yield client
