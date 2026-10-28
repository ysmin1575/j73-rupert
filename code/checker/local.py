"""Local exclusion rules: G, signed-contact SC, and replayed tubes."""
from collections import Counter
from fractions import Fraction as F
from exact import need, fields, index, bounds, decode, Q5, Interval as I
from geometry import Geometry, rotation, mv, mm, sub, dot
from image import frame, derivatives, screen, constraints, label, first_sweep_box
import polynomial as P

RULE_COUNTS = Counter()


def G(box,vertex,direction):
    g = Geometry()
    index(vertex,60)
    need(type(direction) is list and len(direction) == 2, 'screen direction')
    w = [I(x.a) for x in map(decode,direction) if x.b == 0]
    need(len(w) == 2, 'G direction must be rational')
    length = sum((x.square() for x in w),I(0)).sqrt()
    need(length.lo > 0, 'zero direction')
    c,h = [(a+b)/2 for a,b in box],[(b-a)/2 for a,b in box]
    eps = max(h)
    m1,m2 = frame(*c[:2])[:2],frame(*c[2:4])[:2]
    dt1,dp1 = derivatives(*c[:2])
    dt2,dp2 = derivatives(*c[2:4])
    r = tuple(row[:2] for row in screen(c[4])[:2])
    z = mv(mm(r,m1),g.vertices[vertex])
    derivs = [(-z[1],z[0]),mv(mm(r,dt1),g.vertices[vertex]),mv(mm(r,dp1),g.vertices[vertex])]
    # Each angular generator has norm <=1 and each vertex has norm exactly 1.
    # The multivariate Taylor remainder is <= (sum |delta_i|)^2 |w|/2.
    # Three inner angles give 9/2 eps^2; two outer angles give 2 eps^2.
    lower = dot(z,w)-eps*sum((dot(d,w).absolute() for d in derivs),I(0))-F(9,2)*eps*eps*length
    upper = []
    for p in g.vertices:
        upper.append((dot(mv(m2,p),w)+eps*(dot(mv(dt2,p),w).absolute()+dot(mv(dp2,p),w).absolute())+2*eps*eps*length).hi)
    margin = lower.lo-max(upper)
    need(margin > 0, 'G margin not strictly positive')
    return margin


def pose(anchor,axis,triangle,dominant,sign,mode):
    one = P.const(1)
    w = [P.const(x) for x in anchor]
    if triangle is not None:
        need(mode == 'triangle' and len(triangle) == 3, 'triangle chart')
        r,t = P.var(0),P.var(1)
        for j,k in enumerate(i for i in range(3) if i != axis):
            w[k] = P.add(P.const(triangle[0][j]),P.scale(r,triangle[1][j]-triangle[0][j]),P.scale(P.mul(P.add(one,P.scale(r,-1)),t),triangle[2][j]-triangle[0][j]))
    else:
        for j,k in enumerate(i for i in range(3) if i != axis):
            w[k] = P.add(w[k],P.var(j))
    if mode == 'box':
        need(dominant is None and sign is None, 'box cone labels')
        return w,[P.var(i) for i in (2,3,4)]
    index(dominant,3)
    need(type(sign) is int and sign in (-1,1), 'cone sign')
    z = [None]*3
    z[dominant] = P.const(sign)
    for j,k in enumerate(i for i in range(3) if i != dominant):
        z[k] = P.var(j+2)
    return w,[P.mul(P.var(4),x) for x in z]


def signed_gap(a,q,N,u):
    aa = [P.const(x) for x in a]
    H = P.dot(N,[P.const(x) for x in q])
    Na = P.dot(N,aa)
    return P.add(Na,P.scale(H,-1),P.scale(P.dot(P.cross(aa,N),u),2),P.scale(P.mul(P.dot(N,u),P.dot(aa,u)),2),P.scale(P.mul(P.add(Na,H),P.dot(u,u)),-1))


def point(raw):
    need(type(raw) is list and len(raw) == 2, 'view point')
    return tuple(map(decode,raw))


def SC(cert):
    fields(cert,('op','rotation','anchor','axis','triangle','dominant','sign','bounds','contacts','factor','multipliers','label','original_box','constraints','proof'),('mode',))
    need(cert['op'] == 'SC', 'local opcode')
    g,T = Geometry(),rotation(cert['rotation'])
    need(type(cert['anchor']) is list and len(cert['anchor']) == 3, 'anchor')
    anchor = tuple(map(decode,cert['anchor']))
    axis = index(cert['axis'],3)
    need(anchor[axis] != 0, 'zero anchor axis')
    triangle = None if cert['triangle'] is None else [point(x) for x in cert['triangle']]
    mode = cert.get('mode','triangle' if triangle is not None else 'box')
    need(mode in ('triangle','box','cone'), 'pose mode')
    need((triangle is not None) == (mode == 'triangle'), 'triangle mode binding')
    bb = bounds(cert['bounds'],5)
    if mode != 'box':
        need(bb[4][0] >= 0, 'negative radial coordinate')
    if triangle is not None:
        a,b,c = triangle
        need((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]) > 0, 'triangle orientation')
    w,u = pose(anchor,axis,triangle,cert['dominant'],cert['sign'],mode)
    need(type(cert['contacts']) is list and type(cert['multipliers']) is list, 'SC rows')
    weighted,total = {},Q5()
    for row in cert['contacts']:
        fields(row,('outer','inner','weight'),('edge','edge_Q5'))
        outer,inner = index(row['outer'],60),index(row['inner'],60)
        need(('edge' in row) != ('edge_Q5' in row), 'one edge representation')
        if 'edge' in row:
            pair = row['edge']
            need(type(pair) is list and len(pair) == 2 and pair[0] == outer, 'support edge binding')
            edge = sub(g.body[index(pair[1],60)],g.body[index(pair[0],60)])
        else:
            need(type(row['edge_Q5']) is list and len(row['edge_Q5']) == 3, 'edge vector')
            edge = tuple(map(decode,row['edge_Q5']))
        weight = decode(row['weight'])
        need(weight >= 0, 'negative contact weight')
        N = P.cross([P.const(x) for x in edge],w)
        need(not P.dot(N,w), 'normal outside screen')
        H = P.dot(N,[P.const(x) for x in g.body[outer]])
        need(min(P.bernstein(H,bb)) > 0, 'nonpositive support height')
        for p in g.body:
            slack = P.dot(N,[P.const(x) for x in sub(g.body[outer],p)])
            need(min(P.bernstein(slack,bb)) >= 0, 'invalid outer support')
        weighted = P.add(weighted,P.scale(signed_gap(mv(T,g.body[inner]),g.body[outer],N,u),weight))
        total += weight
    gps = []
    if cert['constraints'] is not None:
        need(cert['original_box'] is not None and cert['label'] is not None, 'missing original image binding')
        original = bounds(cert['original_box'],5)
        label(cert['label'])
        if triangle is None:
            rect = bb[:2]
        else:
            # Correlation norm bounds must use the original fan rectangle,
            # not a smaller local triangle's bounding rectangle.
            raw = cert['constraints']
            fields(raw,('data','rectangle'))
            rect = bounds(raw['rectangle'],2)
        raw = cert['constraints']['data'] if triangle is not None else cert['constraints']
        gps = constraints(raw,original,T,cert['label'],anchor,axis,rect,w,u)
    else:
        need(cert['label'] is None and cert['original_box'] is None, 'unused image binding')
    mus = [decode(x) for x in cert['multipliers']]
    need(len(mus) == len(gps) and all(x >= 0 for x in mus), 'constraint multiplier count or sign')
    factor = cert['factor']
    need(total > 0 or not any(factor), 'image exclusion cannot divide by a vanishing factor')
    quotient = P.quotient(weighted,factor,bb)
    B = P.add(quotient,*(P.scale(p,-mu) for p,mu in zip(gps,mus)))
    assumptions = gps[:]
    for i,(lo,hi) in enumerate(bb):
        assumptions.extend((P.add(P.var(i),P.const(-lo)),P.add(P.const(hi),P.scale(P.var(i),-1))))
    strict = P.prove(B,cert['proof'],bb,assumptions)
    need(total > 0 or strict, 'zero contact weight requires strict image exclusion')
    return {'rule':'SC','strict':strict,'contacts':len(cert['contacts'])}


def _verify_leaf(cert):
    need(type(cert) is dict, 'leaf object')
    if cert.get('op') == 'tube':
        from tube import verify
        return verify(cert)
    if cert.get('op') == 'G':
        fields(cert,('op','box','vertex','direction'),('root','path'))
        bb = bounds(cert['box'],5)
        if 'root' in cert or 'path' in cert:
            need('root' in cert and 'path' in cert, 'root and path required together')
            need(first_sweep_box(cert['root'],cert['path']) == bb, 'first sweep leaf domain binding')
        return {'rule':'G','margin':str(G(bb,cert['vertex'],cert['direction']))}
    return SC(cert)


def verify_leaf(cert):
    result = _verify_leaf(cert)
    RULE_COUNTS[result['rule']] += 1
    return result
