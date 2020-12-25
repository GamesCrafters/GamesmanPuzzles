import json

import pytest
import tempfile

from server import app
from puzzlesolver.puzzles import PuzzleManager

def test_default_path(client):
    rv = client.get('/')
    d = json.loads(rv.data)
    for puzzle in d['response']['puzzles']:
        assert PuzzleManager.hasPuzzleId(puzzle)