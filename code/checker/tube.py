"""J45 tube replay using only the independent checker's exact arithmetic."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib
import json

from exact import Q5, Interval as I, need, index, fields, rational, decode, bounds, enclosure
from geometry import Geometry, rotation, identity, mm, mv, transpose, dot, cross, sub
from image import frame, screen
import polynomial as P


def vector(raw):
    need(type(raw) is list and len(raw) == 3, 'tube vector')
    return tuple(map(decode, raw))


def interval(raw):
    return bounds([raw], 1)[0]


def matrix_intervals(a):
    return tuple(tuple(enclosure(x) for x in row) for row in a)


@lru_cache(maxsize=1)
def geometry_hash():
    """Reconstruct the original canonical geometry, including index order."""
    g = Geometry()
    phi = Q5(F(1, 2), F(1, 2))
    den = enclosure(phi+2).sqrt()
    z, one = I(0), I(1)
    expected_align = ((z, z, one), (-one/den, enclosure(phi)/den, z),
                      (-enclosure(phi)/den, -one/den, z))
    need(g.align == expected_align, 'tube original alignment')
    powers = [identity()]
    for _ in range(4):
        powers.append(mm(mm(g.turn, g.turn), powers[-1]))
    half = tuple(tuple(Q5((-1 if i < 2 else 1)*int(i == j)) for j in range(3)) for i in range(3))
    need(g.groups == tuple(powers+[mm(half, p) for p in powers]), 'tube original group order')
    record = lambda a: [[str(x.a), str(x.b)] for x in a]
    canonical = dict(
        vertex_order='exact lexicographic parent coordinates; gyrated caps retain parent indices',
        body=[record(p) for p in g.body], gyration=[record(row) for row in g.turn],
        alignment_rows=['(0,0,1)', '(-1,phi,0)/sqrt(phi+2)', '(-phi,-1,0)/sqrt(phi+2)'],
        radius_squared=record([g.radius2])[0],
        rotation_group='D5: T72^k then S2*T72^k, k=0..4; S2=diag(-1,-1,1)')
    # Geometry checks all ten proper matrices against every ordered vertex.
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def poly_vector(a):
    return [P.const(x) for x in a]


def poly_sub(a, b):
    return [P.add(x, P.scale(y, -1)) for x, y in zip(a, b)]


def extrema(p, bb):
    values = P.bernstein(p, bb)
    return min(values), max(values)


def norm_upper(magnitudes):
    return I(sum(enclosure(x*x).hi for x in magnitudes)).sqrt().hi


def contact_region(cert, R):
    g = Geometry()
    anchor = vector(cert['anchor_Q5'])
    axes = cert.get('chart_axes', [0, 1, 2])
    need(type(axes) is list and len(axes) == 3 and
         all(type(k) is int for k in axes) and sorted(axes) == [0, 1, 2], 'tube chart permutation')
    need(anchor[axes[0]] != 0, 'tube zero anchor')
    bb = [interval(cert[k]) for k in ('x_bounds', 'y_bounds')] + [(F(0), F(0))]*3
    w = poly_vector(anchor)
    for j, k in enumerate(axes[1:]):
        w[k] = P.add(w[k], P.var(j))
    need(type(cert['contacts']) is list and len(cert['contacts']) == 4, 'tube four contacts')
    normals, torques = [], []
    for row in cert['contacts']:
        i, j = index(row['outer_vertex'], 60), index(row['inner_vertex'], 60)
        need(mv(R, g.body[j]) == g.body[i], 'tube inexact contact')
        n = P.cross(poly_vector(vector(row['normal_edge_Q5'])), w)
        p = poly_vector(g.body[i])
        need(not P.dot(n, w), 'tube normal outside screen')
        need(extrema(P.dot(n, p), bb)[0] > 0, 'tube nonpositive height')
        for vertex in g.body:
            need(extrema(P.dot(n, poly_vector(sub(g.body[i], vertex))), bb)[0] >= 0,
                 'tube invalid actual support')
        normals.append(n)
        torques.append(P.cross(p, n))
    grid = cert.get('bernstein_grid', 1)
    need(type(grid) is int and 1 <= grid <= 16, 'tube Bernstein grid')
    cells = [[tuple(lo+(hi-lo)*F(i+k, grid) for k in (0, 1))
              for (lo, hi), i in zip(bb[:2], ij)] + bb[2:]
             for ij in product(range(grid), repeat=2)]
    c0 = None
    for omitted in range(4):
        a, b, c = [torques[i] for i in range(4) if i != omitted]
        n = P.cross(poly_sub(b, a), poly_sub(c, a))
        h = P.dot(n, a)
        if extrema(h, cells[0])[1] < 0:
            n, h = [P.scale(x, -1) for x in n], P.scale(h, -1)
        for cell in cells:
            lo = extrema(h, cell)[0]
            need(lo > 0, 'tube tetrahedron facet')
            need(extrema(P.add(h, P.scale(P.dot(n, torques[omitted]), -1)), cell)[0] > 0,
                 'tube tetrahedron orientation')
            magnitudes = [max(abs_q(x) for x in extrema(p, cell)) for p in n]
            den = norm_upper(magnitudes)
            need(den > 0, 'tube zero facet normal')
            lower = enclosure(lo).lo / den
            c0 = lower if c0 is None else min(c0, lower)
    normal2 = max(sum((max(abs_q(x) for x in extrema(p, bb))**2 for p in n), Q5())
                  for n in normals)
    C0 = I(enclosure(g.radius2*normal2).hi).sqrt().hi / 2
    c, C, r = (rational(cert[k]) for k in ('c_raw', 'C_raw', 'r'))
    need(0 < c <= c0 and C >= C0 and 0 < r <= 1 and C*r < c, 'tube barrier/remainder condition')
    return anchor, axes, bb[:2], r


def abs_q(x):
    return x if x >= 0 else -x


def canonical_rotation():
    return rotation([[['1/4', '1/4'], ['-1/4', '1/4'], ['-1/2', '0']],
                     [['1/4', '-1/4'], ['-1/2', '0'], ['-1/4', '-1/4']],
                     [['-1/2', '0'], ['1/4', '1/4'], ['1/4', '-1/4']]])


def intersection_region(cert, R):
    need(R in (identity(), canonical_rotation()), 'tube intersection reference')
    rho = rational(cert['rho'])
    need(0 < rho <= F(1, 100), 'tube intersection support square')
    fields(cert['box'], tuple('abxyz'))
    bb = [interval(cert['box'][key]) for key in 'abxyz']
    need(all(-rho <= lo <= hi <= rho for lo, hi in bb), 'tube intersection cube')
    need(1-7*rho*rho >= F(1, 2) and rho <= F(1, 552), 'tube shift remainder')
    need(F(1, 2)-6*rho-392*rho*rho >= F(1, 4), 'tube cap remainder')
    need(F(1, 8)-14*rho >= F(1, 50) and F(1, 8)-1008*rho >= F(1, 50),
         'tube weighted determinant')
    need(20*(1+3*rho*rho) < 21, 'tube normalization')
    from tube_intersection import replay
    replay()
    return bb


def contains(cert, box, R, data, go, gi, lift):
    g = Geometry()
    c = [(a+b)/2 for a, b in box]
    h = [(b-a)/2 for a, b in box]
    # Original wire order: inner theta/phi, outer theta/phi, screen alpha.
    O = mm(frame(*c[2:4]), g.align)
    inner = mm(mm(screen(c[4]), frame(*c[:2])), g.align)
    Go, Gi = matrix_intervals(g.groups[go]), matrix_intervals(g.groups[gi])
    w = mv(transpose(Go), O[2])
    w = tuple(x+I(-sum(h[2:4]), sum(h[2:4])) for x in w)
    LO = tuple(tuple((-1 if lift and i < 2 else 1)*x for x in row) for i, row in enumerate(O))
    ref = matrix_intervals(R)
    if cert['model'] == 'contact-facet':
        anchor, axes, bb, radius = data
        f = axes[0]
        xy = [enclosure(anchor[f])*w[k]/w[f]-enclosure(anchor[k]) for k in axes[1:]]
        need(all(lo <= x.lo <= x.hi <= hi for (lo, hi), x in zip(bb, xy)), 'tube view outside region')
        expected = mm(mm(mm(LO, Go), ref), transpose(Gi))
        y = (sum(((inner[i][j]-expected[i][j]).square() for i, j in product(range(3), repeat=2)), I(0))/8).sqrt()
        yh = y.hi
        need(yh < F(1, 2), 'tube rotation distance')
        angle = 2*I(yh)/I(1-yh*yh).sqrt()+sum(h)
        need(angle.hi <= radius, 'tube angle outside radius')
    else:
        E = mm(mm(mm(transpose(mm(LO, Go)), inner), Gi), transpose(ref))
        E = tuple(tuple(x+I(-sum(h), sum(h)) for x in row) for row in E)
        den = 1+sum(E[i][i] for i in range(3))
        need(den.lo > 0, 'tube Cayley denominator')
        values = [-w[1]/w[0], -w[2]/w[0]] + [
            (E[2][1]-E[1][2])/den, (E[0][2]-E[2][0])/den, (E[1][0]-E[0][1])/den]
        need(all(lo <= x.lo <= x.hi <= hi for (lo, hi), x in zip(data, values)), 'tube Cayley box outside region')


def reject_floats(raw):
    need(type(raw) is not float, 'tube float input')
    if type(raw) is dict:
        for value in raw.values():
            reject_floats(value)
    elif type(raw) is list:
        for value in raw:
            reject_floats(value)


def verify(cert):
    fields(cert, ('op', 'box', 'region', 'group_out', 'group_in', 'screen_lift'))
    need(cert['op'] == 'tube', 'tube opcode')
    reject_floats(cert)
    box = bounds(cert['box'], 5)
    go, gi, lift = (index(cert[k], n) for k, n in (('group_out', 10), ('group_in', 10), ('screen_lift', 2)))
    region = cert['region']
    need(type(region) is dict and region.get('schema') == 'j45-region-v1', 'tube region schema')
    need(region.get('model') in ('contact-facet', 'astra-intersection'), 'tube region model')
    need(region['input_hash'] == geometry_hash(), 'tube geometry hash')
    R = rotation(region['reference_T_body_Q5'])
    data = contact_region(region, R) if region['model'] == 'contact-facet' else intersection_region(region, R)
    contains(region, box, R, data, go, gi, lift)
    return dict(rule='tube', model=region['model'])
