"""Exact fixed/radial/cap and reflection identities for the J45 mixed rule.

Ported from the Task 45 identities; arithmetic is entirely checker-owned.
The two branches use only the first barrier on e=0; no e>0 division is used.
"""
from fractions import Fraction as F
import itertools
from exact import Q5 as Q, need
from geometry import Geometry, mm, mv, transpose, dot, cross, identity, sub as vector_sub
import polynomial
from tube import canonical_rotation, poly_sub as psub

pc, pv = polynomial.const, polynomial.var
add, mul, scale = polynomial.add, polynomial.mul, polynomial.scale
pdot, pcross = polynomial.dot, polynomial.cross


def neg(a):
    return scale(a, -1)


def sub(a, b):
    return add(a, neg(b))


def replay():
    vertices, T = Geometry().body, canonical_rotation()
    k, l, H = Q(F(3, 2), F(1, 2)), Q(F(5, 2), F(1, 2)), Q(2, 1)
    sr = F(1, 100)
    TP = tuple(mv(T, p) for p in vertices)
    shared = set(vertices) & set(TP)
    need(mm(transpose(T), T) == identity() and dot(T[0], cross(T[1], T[2])) == 1,
         'canonical rotation')
    need(len(vertices) == 60 and all(tuple(-z for z in p) in vertices for p in vertices),
         'central symmetry')
    need(set(TP) == {(-p[0], p[1], p[2]) for p in vertices}, 'TP reflection identity')
    need(all((-p[0], p[1], p[2]) in shared for p in shared), 'common hull reflection')
    # Common midpoints contain the full yz projection, computed by an exact hull.
    points = sorted(set((p[1], p[2]) for p in shared))
    def chain(ps):
        out = []
        for p in ps:
            while len(out) > 1:
                a, b = out[-2:]
                if (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]) > 0:
                    break
                out.pop()
            out.append(p)
        return out
    hull = chain(points)[:-1]+chain(points[::-1])[:-1]
    checks = 0
    for p, q in zip(hull, hull[1:]+hull[:1]):
        ny, nz = q[1]-p[1], p[0]-q[0]
        h = ny*p[0]+nz*p[1]
        for a, b in itertools.product((-sr, sr), repeat=2):
            for z in vertices:
                if z in shared:
                    continue
                need(ny*(z[1]+a*z[0])+nz*(z[2]+b*z[0]) <= h, 'T equality cone invalid')
                checks += 1
    for s in (-1, 1):
        q = (Q(0), s*k, l)
        need(q in shared, 'shared radial point missing')
        for a, b in itertools.product((-sr, sr), repeat=2):
            for n in ((Q(s*a+b), Q(s), Q(1)), (s*k*a+l*b, s*k, l)):
                need(dot(n, q) > 0 and all(dot(n, vector_sub(q, p)) >= 0 for p in vertices),
                     'intersection support invalid')
                checks += 60
    for axis in (1, 2):
        for a in (-sr, F(0), sr):
            n = (Q(a), Q(int(axis == 1)), Q(int(axis == 2)))
            need(max(dot(n, p) for p in vertices) == H+abs(a), 'cap support invalid')
            checks += 60
        for s, t in itertools.product((-1, 1), repeat=2):
            q = (Q(s), H, Q(t)) if axis == 1 else (Q(s), Q(t), H)
            need(q in shared, 'shared cap missing')
    # Verify the shifted fixed/radial polynomials, not a fitted Hessian.
    a, b, x, y, t = [pv(i) for i in range(5)]
    one, u = pc(1), (x, y, neg(t))
    uu = pdot(u, u)
    B = add(scale(mul(y, sub(a, t)), l), scale(mul(t, sub(b, y)), k))
    D = add(one, sub(scale(mul(a, t), l), scale(mul(b, y), k)))
    X = sub(mul(D, x), B)
    A = add(scale(mul(y, sub(b, y)), l), scale(mul(t, sub(a, t)), k),
            scale(mul(x, x), -k-l), scale(mul(mul(a, x), y), k),
            scale(mul(mul(b, x), t), -l))
    for s in (-1, 1):
        q = tuple(pc(z) for z in (Q(0), s*k, l))
        n = (add(scale(a, s), b), pc(s), one)
        f = add(pdot(pcross(q, n), u), mul(pdot(n, u), pdot(q, u)),
                neg(mul(pdot(n, q), uu)))
        need(f == add(A, scale(X, -s)), 'fixed normal identity')
        n = (add(scale(a, s*k), scale(b, l)), pc(s*k), pc(l))
        f = add(pdot(pcross(q, n), u), mul(pdot(n, u), pdot(q, u)),
                neg(mul(pdot(n, q), uu)))
        pred = add(mul(add(scale(t, s*k), scale(y, l)),
                       add(scale(sub(a, t), s*k), scale(sub(b, y), l))),
                   mul(mul(n[0], x), sub(scale(y, s*k), scale(t, l))),
                   scale(mul(x, x), -k*k-l*l))
        need(f == pred, 'radial identity')
    z, DD = neg(t), add(one, uu)
    U = add(mul(b, add(one, mul(x, x), neg(mul(y, y)), neg(mul(z, z)))),
            scale(y, -2), scale(mul(x, z), 2))
    V = scale(add(x, mul(z, sub(y, b)), mul(mul(b, x), y)), 2)
    W = add(one, mul(z, z), neg(mul(x, x)), neg(mul(y, y)),
            scale(mul(b, y), 2), scale(mul(mul(b, x), z), 2))
    n = (b, {}, one)
    for sb, s1, s2 in itertools.product((-1, 1), repeat=3):
        q = tuple(pc(c) for c in (Q(s1), Q(s2), H))
        h = add(pc(H), scale(b, sb))
        Fcap = add(pdot(n, q), neg(h), scale(pdot(pcross(q, n), u), 2),
                   scale(mul(pdot(n, u), pdot(q, u)), 2),
                   neg(mul(add(pdot(n, q), h), uu)))
        pred = sub(add(scale(U, s1), scale(V, s2), scale(W, H)), mul(h, DD))
        need(Fcap == pred, 'signed cap identity')
    # Exact second branch: C(0,b,-a) Rx is reflection in m=(1,-a,-b).
    aa, bb, one2 = pv(0), pv(1), pc(1)
    ub, m = ({}, bb, neg(aa)), (one2, neg(aa), neg(bb))
    ub2 = pdot(ub, ub)
    db = add(one2, ub2)
    skew = (({}, neg(ub[2]), ub[1]), (ub[2], {}, neg(ub[0])), (neg(ub[1]), ub[0], {}))
    for i, j in itertools.product(range(3), repeat=2):
        cij = add(sub(one2, ub2) if i == j else {},
                  scale(mul(ub[i], ub[j]), 2), scale(skew[i][j], 2))
        lhs = scale(cij, -1 if j == 0 else 1)
        rhs = sub(db if i == j else {}, scale(mul(m[i], m[j]), 2))
        need(lhs == rhs, 'second-branch reflection identity')
    need(2 < k < 3 and 3 < l < 4 and k+l < 7 and k*k+l*l < 20 and 4 < H < 5,
         'analytic coefficient bounds')
    selected = [(Q(0), s*k, l) for s in (-1, 1)]
    selected += [(Q(s), Q(t), H) for s, t in itertools.product((-1, 1), repeat=2)]
    selected += [(Q(s), H, Q(t)) for s, t in itertools.product((-1, 1), repeat=2)]
    need(all(p in vertices and p in shared for p in selected), 'identity selected-point transfer')
    return checks
