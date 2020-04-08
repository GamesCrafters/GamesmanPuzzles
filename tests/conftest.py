import pytest
import tempfile

from puzzlesolver.solvers import SqliteSolver
from puzzlesolver.server import app

@pytest.fixture
def client(tmpdir):
    SqliteSolver.DATABASE_DIR = tmpdir
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client