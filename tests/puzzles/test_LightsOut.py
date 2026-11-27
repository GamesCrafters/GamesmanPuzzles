import json
import random

import pytest

from puzzlesolver.puzzles import LightsOut as p_cls
from puzzlesolver.puzzles import PuzzleManager
from puzzlesolver.solvers import LightsOutClosedFormSolver
from puzzlesolver.util import PuzzleValue, PuzzleException, StringMode


########################################################################
# Reference implementation (positions and clicks as strings of '0'/'1')
########################################################################

def crossBits(n):
    """crossBits(n)[m] is the set of cells toggled by clicking cell m, as an
    int whose bit i is cell i of the position string."""
    crosses = []
    for y in range(n):
        for x in range(n):
            bits = 0
            for cx, cy in ((x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= cx < n and 0 <= cy < n:
                    bits |= 1 << (cy * n + cx)
            crosses.append(bits)
    return crosses


def toBits(position):
    return sum(1 << i for i, c in enumerate(position) if c == '1')


def toPosition(bits, n):
    return ''.join('1' if bits >> i & 1 else '0' for i in range(n * n))


def referenceAllRemoteness(n):
    """{position bits: fewest clicks}, by trying every click pattern."""
    crosses = crossBits(n)
    best = {}
    for clicks in range(1 << (n * n)):
        bits = 0
        for m in range(n * n):
            if clicks >> m & 1:
                bits ^= crosses[m]
        w = bin(clicks).count('1')
        if w < best.get(bits, n * n + 1):
            best[bits] = w
    return best


class Elimination:
    """Solves A x = b over GF(2) by Gaussian elimination on A itself."""

    def __init__(self, n):
        self.n = n
        cells = n * n
        crosses = crossBits(n)
        # Row i of A: which clicks toggle cell i. Augment with the identity to
        # track the row operations.
        rows = []
        for i in range(cells):
            row = sum(1 << m for m in range(cells) if crosses[m] >> i & 1)
            rows.append([row, 1 << i])
        pivots = []
        r = 0
        for col in range(cells):
            pivot = next((i for i in range(r, cells) if rows[i][0] >> col & 1), None)
            if pivot is None:
                continue
            rows[r], rows[pivot] = rows[pivot], rows[r]
            for i in range(cells):
                if i != r and rows[i][0] >> col & 1:
                    rows[i][0] ^= rows[r][0]
                    rows[i][1] ^= rows[r][1]
            pivots.append(col)
            r += 1
        self.rows, self.pivots, self.rank = rows, pivots, r
        free = [c for c in range(cells) if c not in pivots]
        self.kernel = []
        for f in free:
            v = 1 << f
            for i, col in enumerate(pivots):
                if rows[i][0] >> f & 1:
                    v |= 1 << col
            self.kernel.append(v)

    def remoteness(self, bits):
        """Fewest clicks for the position, or None if unsolvable."""
        cells = self.n * self.n
        # Apply the recorded row operations to b.
        reduced = [bin(self.rows[i][1] & bits).count('1') & 1 for i in range(cells)]
        if any(reduced[self.rank:]):
            return None
        x0 = sum(1 << col for i, col in enumerate(self.pivots) if reduced[i])
        best = cells + 1
        for c in range(1 << len(self.kernel)):
            v = x0
            for j, k in enumerate(self.kernel):
                if c >> j & 1:
                    v ^= k
            best = min(best, bin(v).count('1'))
        return best


def freshSolver(n):
    LightsOutClosedFormSolver._cache.clear()
    return LightsOutClosedFormSolver(p_cls(variant=str(n)))


def randomSolvablePosition(n, rng):
    crosses = crossBits(n)
    bits = 0
    for m in range(n * n):
        if rng.getrandbits(1):
            bits ^= crosses[m]
    return toPosition(bits, n)


########################################################################
# Puzzle
########################################################################

def testSerialization():
    rng = random.Random(1)
    for n in (2, 3, 7, 12, 30):
        position = randomSolvablePosition(n, rng)
        puzzle = p_cls.fromString(str(n), position)
        assert puzzle.toString(StringMode.HUMAN_READABLE) == position
        assert puzzle.toString(StringMode.AUTOGUI) == '1_' + position
        # The hash is the position string read as a binary number.
        assert p_cls.fromHash(str(n), int(position, 2)).toString(StringMode.HUMAN_READABLE) == position


def testGridMatchesString():
    puzzle = p_cls.fromString('3', '110' '011' '000')
    assert puzzle.grid == [[True, True, False], [False, True, True], [False, False, False]]


def testPrimitive():
    assert p_cls.fromString('3', '1' * 9).primitive() == PuzzleValue.UNDECIDED
    assert p_cls.fromString('3', '0' * 9).primitive() == PuzzleValue.SOLVABLE
    assert p_cls.generateStartPosition('3').generateSolutions()[0].primitive() == PuzzleValue.SOLVABLE


def testMoves():
    rng = random.Random(2)
    for n in (2, 3, 5, 26, 38):
        crosses = crossBits(n)
        position = randomSolvablePosition(n, rng)
        puzzle = p_cls.fromString(str(n), position)
        moves = puzzle.generateMoves(movetype='legal')
        assert len(moves) == n * n and len(set(moves)) == n * n
        for x, y in moves:
            child = puzzle.doMove((x, y))
            expected = toBits(position) ^ crosses[y * n + x]
            assert toBits(child.toString(StringMode.HUMAN_READABLE)) == expected
            assert child.doMove((x, y)).toString(StringMode.HUMAN_READABLE) == position
        assert puzzle.toString(StringMode.HUMAN_READABLE) == position  # unchanged


def testMoveStrings():
    puzzle = p_cls.generateStartPosition('30')
    assert puzzle.moveString((0, 0), StringMode.HUMAN_READABLE) == 'a30'
    assert puzzle.moveString((25, 29), StringMode.HUMAN_READABLE) == 'z1'
    assert puzzle.moveString((26, 29), StringMode.HUMAN_READABLE) == 'aa1'
    assert puzzle.moveString((3, 2), StringMode.AUTOGUI) == 'A_t_63_x'


def testValidation():
    unsolvable4 = next(toPosition(b, 4) for b in range(1 << 16)
                       if Elimination(4).remoteness(b) is None)
    invalid = [
        ('', '3'),                      # wrong length
        ('1' * 9, '2'),                 # wrong length for the variant
        ('1' * 8, '3'),                 # too short
        ('1' * 10, '3'),                # too long
        ('10201' '0000', '3'),          # bad character
        ('1' * 9, '1'),                 # unsupported variant
        ('1' * 1521, '39'),             # unsupported variant
        (unsolvable4, '4'),             # cannot be solved
    ]
    for position, variant in invalid:
        with pytest.raises(PuzzleException):
            PuzzleManager.validate(p_cls.id, variant, position)
    PuzzleManager.validate(p_cls.id, '4', '1' * 16)  # all lit is always solvable


def testVariants():
    assert p_cls.variants == [str(n) for n in range(2, 39)]
    for variant in p_cls.variants:
        assert PuzzleManager.getSolverClass(p_cls.id, variant) is LightsOutClosedFormSolver


########################################################################
# Solver
########################################################################

@pytest.mark.parametrize("n", [2, 3, 4])
def testRemotenessExhaustive(n):
    reference = referenceAllRemoteness(n)
    solver = freshSolver(n)
    for bits, remoteness in reference.items():
        puzzle = p_cls.fromString(str(n), toPosition(bits, n))
        assert solver.getRemoteness(puzzle) == remoteness
    # Every other position is rejected as unsolvable.
    solvable = set(reference)
    for bits in range(1 << (n * n)):
        if bits not in solvable:
            with pytest.raises(ValueError):
                p_cls.fromString(str(n), toPosition(bits, n))


@pytest.mark.parametrize("n", [5, 6, 9, 11, 14, 16, 17, 19])
def testRemotenessAgainstElimination(n):
    rng = random.Random(n)
    reference = Elimination(n)
    for _ in range(4):
        position = randomSolvablePosition(n, rng)
        solver = freshSolver(n)
        assert solver.getRemoteness(p_cls.fromString(str(n), position)) == \
            reference.remoteness(toBits(position))


@pytest.mark.parametrize("n", [4, 5, 9, 11, 16])
def testChildrenFromOneSearch(n):
    """The children's remoteness, filled in by the parent's search, is exact."""
    rng = random.Random(100 + n)
    reference = Elimination(n)
    for _ in range(2):
        solver = freshSolver(n)
        puzzle = p_cls.fromString(str(n), randomSolvablePosition(n, rng))
        solver.getRemoteness(puzzle)
        for move in puzzle.generateMoves():
            child = puzzle.doMove(move)
            assert solver.getRemoteness(child) == \
                reference.remoteness(toBits(child.toString(StringMode.HUMAN_READABLE)))


def testSeveralClicksInARow():
    """Walks a game the way the server asks: position first, then every child."""
    n = 9
    rng = random.Random(7)
    reference = Elimination(n)
    solver = freshSolver(n)
    puzzle = p_cls.fromString(str(n), randomSolvablePosition(n, rng))
    for _ in range(4):
        assert solver.getRemoteness(puzzle) == \
            reference.remoteness(toBits(puzzle.toString(StringMode.HUMAN_READABLE)))
        moves = puzzle.generateMoves()
        children = [puzzle.doMove(move) for move in moves]
        values = [solver.getRemoteness(child) for child in children]
        for child, value in zip(children[:10], values[:10]):
            assert value == reference.remoteness(toBits(child.toString(StringMode.HUMAN_READABLE)))
        puzzle = children[rng.randrange(len(children))]


def testRandomStartIsSolvable():
    for n in (2, 4, 5, 9, 30, 32, 38):
        solver = freshSolver(n)
        for _ in range(5):
            puzzle = p_cls.fromHash(str(n), solver.getRandomSolvableHash())
            position = puzzle.toString(StringMode.HUMAN_READABLE)
            assert '1' in position
            p_cls.fromString(str(n), position)  # raises if unsolvable


def testNullity():
    from puzzlesolver.solvers.lightsoutclosedformsolver import getMath
    expected = {4: 4, 5: 2, 9: 8, 11: 6, 14: 4, 16: 8, 17: 2, 19: 16, 23: 14, 24: 4, 29: 10, 30: 20,
                32: 20, 33: 16, 34: 4, 35: 6}
    for n in range(2, 39):
        assert getMath(n).nullity == expected.get(n, 0)


########################################################################
# Server
########################################################################

def testServerRoute():
    from scripts.server.src.routes import app
    client = app.test_client()
    n = 5
    rng = random.Random(3)
    reference = Elimination(n)
    LightsOutClosedFormSolver._cache.clear()

    position = randomSolvablePosition(n, rng)
    rv = client.get('/lightsout/{}/positions/?p={}'.format(n, position))
    assert rv.status_code == 200
    d = json.loads(rv.data)
    assert d['positionValue'] == PuzzleValue.SOLVABLE
    assert d['remoteness'] == reference.remoteness(toBits(position))
    assert len(d['moves']) == n * n
    for move in d['moves']:
        assert move['positionValue'] == PuzzleValue.SOLVABLE
        assert move['remoteness'] == reference.remoteness(toBits(move['position']))

    rv = client.get('/lightsout/{}/start/'.format(n))
    assert rv.status_code == 200
    start = json.loads(rv.data)['position']
    assert reference.remoteness(toBits(start)) is not None

    # The server reports errors as {'error': ...} (its 404 handler returns status 200).
    for bad in ('1' * 15, '1' * 16 + '0', '2' * 16):
        d = json.loads(client.get('/lightsout/4/positions/?p={}'.format(bad)).data)
        assert 'Invalid PositionID' in d['error']
