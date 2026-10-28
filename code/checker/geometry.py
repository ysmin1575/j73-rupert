"""Exact J73 vertex order, proper D5 action and translation hypotheses."""
from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache
from exact import Q5, decode, need, enclosure, Interval as I


def dot(a,b):
    need(len(a) == len(b), 'vector dimensions')
    return sum((x*y for x,y in zip(a,b)),0)


def cross(a,b):
    return tuple(a[(i+1)%3]*b[(i+2)%3]-a[(i+2)%3]*b[(i+1)%3] for i in range(3))


def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))


def transpose(a):
    return tuple(zip(*a))


def mv(a,x):
    return tuple(dot(row,x) for row in a)


def mm(a,b):
    return tuple(tuple(dot(row,col) for col in transpose(b)) for row in a)


def identity():
    return tuple(tuple(Q5(int(i == j)) for j in range(3)) for i in range(3))


def rotation(raw):
    need(type(raw) is list and len(raw) == 3 and all(type(r) is list and len(r) == 3 for r in raw), 'rotation shape')
    a = tuple(tuple(decode(x) for x in r) for r in raw)
    need(mm(transpose(a),a) == identity() and dot(a[0],cross(a[1],a[2])) == 1, 'not SO(3)')
    return a


@lru_cache(maxsize=1)
class Geometry:
    def __init__(self):
        phi = Q5(F(1,2),F(1,2))
        parent = set()
        for seed in ((Q5(1),Q5(1),phi**3),(phi**2,phi,2*phi),(2+phi,Q5(),phi**2)):
            for signs in product((-1,1),repeat=3):
                p = tuple(s*x for s,x in zip(signs,seed))
                parent.update(p[k:]+p[:k] for k in range(3))
        parent = sorted(parent)
        need(len(parent) == 60, 'parent count')
        axis = (-phi,Q5(-1),Q5())
        c,s = phi/2,Q5(F(-1,4),F(1,4))
        skew = ((0,-axis[2],axis[1]),(axis[2],0,-axis[0]),(-axis[1],axis[0],0))
        turn = tuple(tuple(c*int(i==j)+s*skew[i][j]+(1-c)*axis[i]*axis[j]/dot(axis,axis) for j in range(3)) for i in range(3))
        need(mm(transpose(turn),turn) == identity(), 'cap rotation')
        self.turn = turn
        levels = [dot(axis,p) for p in parent]
        cap = max(levels)
        need(sum(t in (cap,-cap) for t in levels) == 10, 'two pentagonal caps')
        self.body = tuple(mv(turn,p) if t == cap else mv(transpose(turn),p) if t == -cap else p for p,t in zip(parent,levels))
        lookup = {p:i for i,p in enumerate(self.body)}
        need(len(lookup) == 60, 'duplicate vertex')
        self.radius2 = Q5(11,4)
        need(all(dot(p,p) == self.radius2 for p in self.body), 'common circumradius')
        need(all(tuple(-x for x in p) in lookup for p in self.body), 'central symmetry')
        need(any(dot(a,cross(b,c)) != 0 for a,b,c in combinations(self.body,3)), 'three dimensional body')
        powers = [identity()]
        for _ in range(4):
            powers.append(mm(mm(turn,turn),powers[-1]))
        need(mm(mm(turn,turn),powers[-1]) == identity(), 'order five')
        half = ((Q5(-1),Q5(),Q5()),(Q5(),Q5(-1),Q5()),(Q5(),Q5(),Q5(1)))
        need(all(mv(h,axis) == axis for h in powers) and mv(half,axis) == tuple(-x for x in axis), 'D5 polar reduction')
        self.groups = tuple(powers+[mm(half,a) for a in powers])
        self.permutations = []
        for a in self.groups:
            need(mm(transpose(a),a) == identity() and dot(a[0],cross(a[1],a[2])) == 1, 'proper symmetry')
            need(all(mv(a,p) in lookup for p in self.body), 'symmetry image')
            self.permutations.append(tuple(lookup[mv(a,p)] for p in self.body))
        need(len(set(self.permutations)) == 10, 'faithful D5')
        # Conv(P) and its linear projections are centrally symmetric convex
        # sets. If K+t is strictly inside L, symmetry also gives K-t inside;
        # averaging these two points removes t by convexity of int(L).
        den = enclosure(phi+2).sqrt()
        z,o = I(0),I(1)
        self.align = ((z,z,o),(-o/den,enclosure(phi)/den,z),(-enclosure(phi)/den,-o/den,z))
        radius = enclosure(self.radius2).sqrt()
        self.vertices = tuple(tuple(x/radius for x in mv(self.align,tuple(enclosure(q) for q in p))) for p in self.body)
        self.pole = (-phi,Q5(-1),Q5())
