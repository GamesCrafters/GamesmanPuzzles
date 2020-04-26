import json

import pytest
import tempfile

from puzzlesolver.server import app
from puzzlesolver.puzzles import puzzleList

@pytest.fixture
def client():
    app.config['TESTING'] = True
    dir_path = tempfile.mkdtemp()
    app.config['DATABASE_DIR'] = dir_path

    for p_cls in puzzleList.values():
        if hasattr(p_cls, 'test_variants'):
            variants = p_cls.test_variants
        else: 
            variants = p_cls.variants
        for variant in variants:
            s_cls = variants[variant]
            puzzle = p_cls.generateStartPosition(variant)
            solver = s_cls(puzzle, dir_path=dir_path)
            solver.solve()

    with app.test_client() as client:
        yield client

def test_default_path(client):
    rv = client.get('/')
    d = json.loads(rv.data)
    for puzzle in d['response']['puzzles']:
        assert puzzle in puzzleList