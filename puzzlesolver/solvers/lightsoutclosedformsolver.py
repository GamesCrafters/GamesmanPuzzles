import random
import threading
from collections import OrderedDict

from .solver import Solver
from ..util import *


# Gray-code search chunk: the lowest CHUNK_BITS basis vectors are combined into
# a table of up to 2^CHUNK_BITS patterns that is scanned in one comprehension.
CHUNK_BITS = 10

# Number of remoteness values kept in the shared cache (all board sizes).
# Each click adds n^2 + 1 values; when full at 38x38 this is about 25 MB.
CACHE_SIZE = 50_000

# Number of 1 bits in an int. int.bit_count needs Python 3.10; setup.py allows
# 3.6, so older versions fall back to counting the characters of bin().
if hasattr(int, "bit_count"):
    _popcount = int.bit_count
else:
    def _popcount(value):
        return bin(value).count("1")


###########################################################################
# Polynomials over GF(2), stored as ints (bit i is the coefficient of x^i)
###########################################################################

def _degree(p):
    return p.bit_length() - 1


def _divmod(a, b):
    """Quotient and remainder of a / b."""
    q = 0
    db = _degree(b)
    while a and _degree(a) >= db:
        shift = _degree(a) - db
        q |= 1 << shift
        a ^= b << shift
    return q, a


def _multiply(a, b):
    if _popcount(a) < _popcount(b):
        a, b = b, a  # loop over the operand with fewer terms
    result = 0
    while b:
        low = b & -b
        result ^= a << (low.bit_length() - 1)
        b ^= low
    return result


def _gcd_and_multiplier(a, m):
    """Returns (g, s) with g = gcd(a, m) and s * a = g (mod m)."""
    r0, r1, s0, s1 = a, m, 1, 0
    while r1:
        q, r = _divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, s0 ^ _multiply(q, s1)
    return r0, _divmod(s0, m)[1]


###########################################################################
# Per-size setup
###########################################################################

class LightsOutMath:
    """Everything that depends only on the board size n."""

    def __init__(self, n):
        self.n = n
        self.cells = n * n
        self.mask = (1 << n) - 1

        # chi = q_{n+1}(x) and p = q_{n+1}(x + 1) by the same recurrence.
        q0, q1, p0, p1 = 0, 1, 0, 1
        for _ in range(n):
            q0, q1 = q1, (q1 << 1) ^ q0
            p0, p1 = p1, (p1 << 1) ^ p1 ^ p0
        self.chi = q1
        c = _divmod(p1, self.chi)[1]
        self.g, self.multiplier = _gcd_and_multiplier(c, self.chi)
        self.nullity = _degree(self.g)

        # Homogeneous solutions, one per unit of nullity.
        self.basis = []
        line = self.toLine(_divmod(self.chi, self.g)[0])
        for _ in range(self.nullity):
            self.basis.append(self.flatten(self.chase(None, line)[:n]))
            line = self.neighbours(line)

        # crosses[y * n + x] is the flat set of cells toggled by clicking (x, y).
        self.crosses = []
        for y in range(n):
            for x in range(n):
                rows = [0] * n
                rows[y] = self.sameRow(1 << x)
                if y > 0:
                    rows[y - 1] = 1 << x
                if y < n - 1:
                    rows[y + 1] = 1 << x
                self.crosses.append(self.flatten(rows))

    # Row operations -------------------------------------------------------

    def neighbours(self, row):
        """M row: each cell's left and right neighbours."""
        return ((row << 1) ^ (row >> 1)) & self.mask

    def sameRow(self, clicks):
        """Cells toggled in a row by clicking `clicks` in that row."""
        return self.neighbours(clicks) ^ clicks

    def flatten(self, rows):
        flat = 0
        for y, row in enumerate(rows):
            flat |= row << (y * self.n)
        return flat

    def chase(self, rows, top):
        """Clicks `top` in the first row, then chases the lights down.

        Returns n + 1 rows of clicks: the click rows for the board, plus the
        clicks the leftover bottom row would need from a row below the board.
        `rows=None` chases an all-off board."""
        clicks = [top]
        previous, current = 0, top
        for y in range(self.n):
            below = self.sameRow(current) ^ previous
            if rows is not None:
                below ^= rows[y]
            clicks.append(below)
            previous, current = current, below
        return clicks

    # Line <-> polynomial ---------------------------------------------------

    def toPolynomial(self, line):
        """Cell j of a row is q_{j+1}(M) e_0."""
        p = 0
        q0, q1 = 0, 1
        for j in range(self.n):
            if line >> j & 1:
                p ^= q1
            q0, q1 = q1, (q1 << 1) ^ q0
        return p

    def toLine(self, p):
        """p(M) e_0, by Horner's rule."""
        line = 0
        for j in range(_degree(p), -1, -1):
            line = self.neighbours(line)
            if p >> j & 1:
                line ^= 1
        return line

    # Solving ---------------------------------------------------------------

    def firstRowClicks(self, rows):
        """First-row clicks of one solution, or None if unsolvable."""
        leftover = self.chase(rows, 0)[self.n]
        quotient, remainder = _divmod(self.toPolynomial(leftover), self.g)
        if remainder:
            return None
        t = _divmod(_multiply(self.multiplier, quotient), self.chi)[1]
        return self.toLine(t)

    def isSolvable(self, rows):
        return self.firstRowClicks(rows) is not None

    def anySolution(self, rows):
        """One solution as a flat click pattern, or None if unsolvable."""
        top = self.firstRowClicks(rows)
        if top is None:
            return None
        return self.flatten(self.chase(rows, top)[:self.n])

    def search(self, rows):
        """Returns (best, optimal, nearOptimal) or None if unsolvable.

        best        -- fewest clicks of any solution (the remoteness)
        optimal     -- OR of every solution with `best` clicks
        nearOptimal -- OR of every solution with `best + 1` clicks"""
        x0 = self.anySolution(rows)
        if x0 is None:
            return None
        k = self.nullity
        if k == 0:
            return _popcount(x0), x0, 0

        # Table of every combination of the lowest `low` basis vectors.
        low = min(k, CHUNK_BITS)
        table = [0]
        for vector in self.basis[:low]:
            table += [t ^ vector for t in table]
        high = self.basis[low:]

        best = self.cells + 2
        optimal = nearOptimal = 0
        base = x0
        for step in range(1 << len(high)):
            if step:
                base ^= high[(step & -step).bit_length() - 1]
            weights = [_popcount(base ^ t) for t in table]
            if min(weights) > best + 1:
                continue
            for t, w in zip(table, weights):
                if w > best + 1:
                    continue
                v = base ^ t
                if w < best:
                    nearOptimal = optimal if w == best - 1 else 0
                    best, optimal = w, v
                elif w == best:
                    optimal |= v
                else:
                    nearOptimal |= v
        return best, optimal, nearOptimal

    # Random positions --------------------------------------------------------

    def randomSolvable(self, rng=random):
        """A random solvable, unsolved position (flat), by random clicks."""
        n = self.n
        while True:
            clicks = [rng.getrandbits(n) for _ in range(n)]
            rows = []
            for y in range(n):
                row = self.sameRow(clicks[y])
                if y > 0:
                    row ^= clicks[y - 1]
                if y < n - 1:
                    row ^= clicks[y + 1]
                rows.append(row)
            flat = self.flatten(rows)
            if flat:
                return flat


_mathBySize = {}
_mathLock = threading.Lock()


def getMath(n):
    """Shared LightsOutMath for size n (built once, on first use)."""
    math = _mathBySize.get(n)
    if math is None:
        with _mathLock:
            math = _mathBySize.get(n)
            if math is None:
                math = _mathBySize[n] = LightsOutMath(n)
    return math


###########################################################################
# Solver
###########################################################################

class LightsOutClosedFormSolver(Solver):
    """Closed-form remoteness for Lights Out.

    Nothing is stored on disk: `path` is "closed_form", which the server
    treats as always available, and `solve` does nothing."""

    # (n, flat position) -> [remoteness, expanded], least recently used first.
    # `expanded` means the remoteness of every child is also in the cache.
    _cache = OrderedDict()
    _cacheLock = threading.Lock()

    def __init__(self, puzzle, **kwargs):
        self.puzzle = puzzle
        self.path = "closed_form"
        getMath(puzzle.size)

    def solve(self, *args, **kwargs):
        return

    def getRandomSolvableHash(self):
        """Hash (as used by LightsOut.fromHash) of a random solvable position."""
        n = self.puzzle.size
        flat = getMath(n).randomSolvable()
        # fromHash reads the hash as the position string in binary, first cell
        # as the most significant bit.
        return int(format(flat, "0{}b".format(n * n)), 2)

    def getRemoteness(self, puzzle, *args, **kwargs):
        math = getMath(puzzle.size)
        key = (puzzle.size, math.flatten(puzzle.rows))
        cls = type(self)

        with cls._cacheLock:
            entry = cls._cache.get(key)
            if entry is not None:
                cls._cache.move_to_end(key)
                return entry[0]

        # Not cached. It is usually a child of the position the server just
        # asked about, which is cached (from the previous click) but not yet
        # expanded: expand that parent, which fills in this position too.
        target = None
        with cls._cacheLock:
            for cross in math.crosses:
                parent = cls._cache.get((puzzle.size, key[1] ^ cross))
                if parent is not None and not parent[1]:
                    target = key[1] ^ cross
                    break
        if target is None:
            target = key[1]

        remoteness = self._expand(math, target)
        if target == key[1]:
            return remoteness
        with cls._cacheLock:
            entry = cls._cache.get(key)
        if entry is not None:
            return entry[0]
        return self._expand(math, key[1])  # evicted in between (rare)

    def _expand(self, math, flat):
        """Searches `flat` once and caches it and all of its children."""
        n = math.n
        rows = [(flat >> (y * n)) & math.mask for y in range(n)]
        result = math.search(rows)
        if result is None:
            return PuzzleValue.MAX_REMOTENESS
        best, optimal, nearOptimal = result

        values = [(flat, best, True)]
        for m, cross in enumerate(math.crosses):
            if optimal >> m & 1:
                child = best - 1
            elif nearOptimal >> m & 1:
                child = best
            else:
                child = best + 1
            values.append((flat ^ cross, child, False))

        cls = type(self)
        with cls._cacheLock:
            for position, value, expanded in values:
                key = (n, position)
                entry = cls._cache.get(key)
                if entry is None:
                    cls._cache[key] = [value, expanded]
                else:
                    entry[1] = entry[1] or expanded
                    cls._cache.move_to_end(key)
            while len(cls._cache) > CACHE_SIZE:
                cls._cache.popitem(last=False)
        return best
