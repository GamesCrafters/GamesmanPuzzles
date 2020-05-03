import json

import pytest
import tempfile

from puzzlesolver.server import app
from puzzlesolver.puzzles import puzzleList

def test_default_path(client):
    rv = client.get('/')
    d = json.loads(rv.data)
    for puzzle in d['response']['puzzles']:
        assert puzzle in puzzleList