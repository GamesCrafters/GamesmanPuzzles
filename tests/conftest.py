import pytest
import tempfile

from puzzlesolver.solvers.gzipsolver import GZipSolver
from puzzlesolver.server import app

@pytest.fixture
def client(tmpdir):
    GZipSolver.DATABASE_DIR = tmpdir
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client