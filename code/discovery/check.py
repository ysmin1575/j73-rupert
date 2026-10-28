"""Independent exact checks for note.tex; Python standard library only.

Run: python -B check.py. No production modules, numerical libraries, workers,
or external executables are used. This program only reads files.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import product
from math import isqrt
from pathlib import Path
from collections import Counter
import json
import time


@dataclass(frozen=True)
class Q:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    def __add__(self, other):
        other = other if isinstance(other, Q) else Q(other)
        return Q(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q) else Q(-other))

    def __rsub__(self, other):
        return Q(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Q) else Q(other)
        return Q(self.a*other.a + 5*self.b*other.b,
                 self.a*other.b + self.b*other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Q) else Q(other)
        d = other.a*other.a - 5*other.b*other.b
        return self * Q(other.a/d, -other.b/d)

    def sign(self):
        if self == Q():
            return 0
        # Certified rational brackets, rather than floating-point evaluation.
        digits = 16
        while True:
            scale = 10**digits
            lo = F(isqrt(5*scale*scale), scale)
            hi = lo + F(1, scale)
            ends = (self.a + self.b*lo, self.a + self.b*hi)
            if min(ends) > 0:
                return 1
            if max(ends) < 0:
                return -1
            digits *= 2


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return tuple(a[(i+1)%3]*b[(i+2)%3] - a[(i+2)%3]*b[(i+1)%3]
                 for i in range(3))


def tr(a):
    return tuple(zip(*a))


def mv(a, v):
    return tuple(dot(row, v) for row in a)


def mm(a, b):
    return tuple(tuple(dot(row, col) for col in tr(b)) for row in a)


def det(a):
    return dot(a[0], cross(a[1], a[2]))


def compare(a, b):
    return next(((x-y).sign() for x, y in zip(a, b) if x != y), 0)


def main():
    start = time.monotonic()
    data = json.loads(Path(__file__).with_name('evidence.json').read_text('utf-8'))
    s = Q(0, 1)
    p = (1+s)/2
    identity = tuple(tuple(Q(int(i == j)) for j in range(3)) for i in range(3))
    seeds = ((Q(1), Q(1), p*p*p), (p*p, p, 2*p), (2+p, Q(), p*p))
    parent = set()
    for seed in seeds:
        for signs in product((-1, 1), repeat=3):
            v = tuple(x*t for x, t in zip(seed, signs))
            parent.update(v[i:]+v[:i] for i in range(3))
    parent = sorted(parent, key=cmp_to_key(compare))
    assert len(parent) == 60
    G = tuple(tuple(Q(*x) for x in row) for row in data['gyration'])
    assert mm(tr(G), G) == identity and det(G) == Q(1)
    axis = (-p, Q(-1), Q())
    assert mv(G, axis) == axis and sum(G[i][i] for i in range(3)) == 1+p
    heights = [dot(axis, v) for v in parent]
    top = max(heights, key=cmp_to_key(lambda x, y: (x-y).sign()))
    levels = sorted(set(heights), key=cmp_to_key(lambda x,y:(x-y).sign()))
    rim = {v for v,h in zip(parent,heights) if h == levels[-2]}
    assert len(rim) == 10 and {mv(G,v) for v in rim} == rim
    V = [mv(G, v) if h == top else mv(tr(G), v) if h == -top else v
         for h, v in zip(heights, parent)]
    assert sum(h == top or h == -top for h in heights) == 10
    assert len(set(V)) == 60 and set(V) == {tuple(-x for x in v) for v in V}
    assert all(dot(v, v) == Q(11, 4) for v in V)
    # The geometric input is a data cross-check, never an imported constructor.
    assert V == [tuple(Q(*x) for x in row) for row in data['body']]
    T = tuple(tuple(x/4 for x in row) for row in (
        (1+s, s-1, Q(-2)), (1-s, Q(-2), -1-s), (Q(-2), 1+s, 1-s)))
    assert mm(tr(T), T) == identity and det(T) == Q(1)
    assert mm(mm(T, T), T) == identity and T != identity
    assert sum(T[i][i] for i in range(3)) == Q()
    assert {mv(T, v) for v in parent} == set(parent)
    TV = {mv(T, v) for v in V}
    common, union = set(V) & TV, set(V) | TV
    assert len(common) == 40 and len(union) == 80
    # H = -T gives the same vertex set, by central symmetry.
    assert TV == {tuple(-x for x in v) for v in TV}
    w = tuple(Q(F(x)) for x in data['view'])
    h = data['boundary']
    assert h == [22,28,16,20,32,33,41,29,35,37,31,43,39,27,26,18,30,24]
    assert len(set(h)) == 18 and all(V[i] in common for i in h)
    distances = [dot(sub(a,b),sub(a,b)) for i,a in enumerate(V) for b in V[i+1:]]
    assert min(distances, key=cmp_to_key(lambda a,b:(a-b).sign())) == Q(4)
    signs = Counter()
    positive_values = []
    for i, j in zip(h, h[1:]+h[:1]):
        for z in union:
            normal = cross(sub(V[j], V[i]), sub(z, V[i]))
            sign = dot(w, normal).sign()
            assert sign >= 0
            assert sign != 0 or normal == (Q(),)*3
            signs[sign] += 1
            if sign > 0:
                positive_values.append(dot(w, normal))
    assert signs == {1: 1404, 0: 36}
    assert min(positive_values, key=cmp_to_key(lambda a,b:(a-b).sign())) == Q(F(-1470249,1048576), F(730489,1048576))
    # Strict convexity and a nondegenerate oriented projection of the cycle.
    for i in range(18):
        a, b, c = (V[h[(i+k)%18]] for k in range(3))
        assert dot(w, cross(sub(b, a), sub(c, b))).sign() > 0
    print('PASS cone: 1440 exact signs = 1404 positive + 36 vector zeros')
    S = ((Q(-1),Q(),Q()), (Q(),Q(-1),Q()), (Q(),Q(),Q(1)))
    R = mm(G, G)
    powers = [identity]
    for _ in range(4):
        powers.append(mm(powers[-1], R))
    D = powers + [mm(S, a) for a in powers]
    assert len(set(D)) == 10 and mm(powers[-1], R) == identity
    assert mm(S, S) == identity and mm(mm(S, R), S) == tr(R)
    assert all(det(a) == Q(1) and mm(tr(a), a) == identity for a in D)
    assert all({mv(a, v) for v in V} == set(V) for a in D)
    pairs = [(a, mm(mm(a, T), tr(b))) for a in D for b in D]
    orbit = Counter(U for _, U in pairs)
    assert len(orbit) == 50 and set(orbit.values()) == {2}
    assert not set(orbit).intersection(D)
    assert tr(T) in orbit
    assert all(len(set(V) & {mv(U, v) for v in V}) == 40 for U in orbit)
    labels = {(tuple(sign*x for x in mv(a, w)), U, lift)
              for a, U in pairs for sign in (-1,1) for lift in (0,1)}
    assert len(labels) == 400
    print('PASS rotations: order 3, parent 60/60, J73 40/60; orbit 50, labels 400')
    torques, weights = [], []
    for contact in data['contacts']:
        v = V[contact['vertex']]
        n = tuple(Q(*x) for x in contact['normal_Q5'])
        weight = Q(*contact['weight_Q5'])
        assert v in common and dot(n, w) == Q() and weight.sign() > 0
        assert all(dot(n, sub(v, x)).sign() > 0 for x in V if x != v)
        assert all(dot(n, sub(v, x)).sign() >= 0 for x in union)
        torques.append(cross(v, n))
        weights.append(weight)
    assert len(torques) == 4 and sum(weights) == Q(1)
    assert all(sum(t[k]*a for t, a in zip(torques, weights)) == Q() for k in range(3))
    assert det(torques[:3]).sign() != 0
    print('PASS anchor: four unique supports, positive weights summing to 1, zero torque sum, rank 3')
    print(f'ALL CHECKS PASS; single process; elapsed {time.monotonic()-start:.3f} s')


if __name__ == '__main__':
    main()
