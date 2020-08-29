import json

import pytest

from puzzlesolver.server import app
from puzzlesolver.puzzles import puzzleList

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_default_path(client):
    rv = client.get('/puzzles/')
    d = json.loads(rv.data)
    for puzzle in d['response']['puzzles']:
        assert puzzle in puzzleList