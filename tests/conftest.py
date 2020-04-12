import pytest
import tempfile

from puzzlesolver.solvers import DATABASE_DIR
from puzzlesolver.server import app

@pytest.fixture
def client(tmpdir):
    global DATABASE_DIR
    DATABASE_DIR = tmpdir
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client