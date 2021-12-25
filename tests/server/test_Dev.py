import json

import pytest
import tempfile

from scripts.server import app
from puzzlesolver.puzzles import PuzzleManager

def test_default_path(client):
    rv = client.get('/')
    d = json.loads(rv.data)
    for puzzle in d['response']:
        assert PuzzleManager.hasPuzzleId(puzzle["gameId"])