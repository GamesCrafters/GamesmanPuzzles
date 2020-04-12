import pytest
import tempfile

import puzzlesolver.solvers
from puzzlesolver.server import app

@pytest.fixture
def client(tmpdir):
    puzzlesolver.solvers.DATABASE_DIR = tmpdir
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client