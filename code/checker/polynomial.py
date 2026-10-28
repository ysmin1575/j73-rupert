"""Sparse Q(sqrt(5)) polynomials and explicit nonnegativity certificates."""
from fractions import Fraction as F
from itertools import product
from math import comb
from exact import Q5, decode, need, fields, index, ResourceLimit

D = 5


def const(x):
    return {(0,)*D: Q5.coerce(x)} if x != 0 else {}


def var(i):
    k = [0]*D
    k[index(i,D)] = 1
    return {tuple(k): Q5(1)}


def clean(p):
    return {k: Q5.coerce(x) for k,x in p.items() if x != 0}


def add(*ps):
    out = {}
    for p in ps:
        for k,x in p.items():
            out[k] = out.get(k,Q5())+x
    return clean(out)


def scale(p, x):
    return clean({k:v*x for k,v in p.items()})


def mul(p, q):
    out = {}
    for k,x in p.items():
        for l,y in q.items():
            key = tuple(a+b for a,b in zip(k,l))
            out[key] = out.get(key,Q5())+x*y
    return clean(out)


def dot(a,b):
    need(len(a) == len(b), 'dot dimensions')
    return add(*(mul(x,y) for x,y in zip(a,b)))


def cross(a,b):
    return [add(mul(a[(i+1)%3],b[(i+2)%3]),scale(mul(a[(i+2)%3],b[(i+1)%3]),-1)) for i in range(3)]


def parse(raw):
    need(type(raw) is list, 'polynomial terms')
    out = {}
    for row in raw:
        need(type(row) is list and len(row) == 2, 'polynomial term')
        k,v = row
        need(type(k) is list and len(k) == D and all(type(n) is int and 0 <= n <= 64 for n in k), 'exponents')
        k = tuple(k)
        need(k not in out, 'duplicate monomial')
        out[k] = decode(v)
    return clean(out)


def restrict(p, bounds):
    out = {}
    for k,x in p.items():
        key = list(k)
        for i,(lo,hi) in enumerate(bounds):
            if lo == hi:
                x *= lo**key[i]
                key[i] = 0
        key = tuple(key)
        out[key] = out.get(key,Q5())+x
    return clean(out)


def substitute(p, xs):
    need(len(xs) == D, 'substitution dimension')
    out = {}
    for k,x in p.items():
        term = const(x)
        for n,q in zip(k,xs):
            for _ in range(n):
                term = mul(term,q)
        out = add(out,term)
    return out


def quotient(p, factor, bounds):
    need(type(factor) is list and len(factor) == D and all(type(n) is int and 0 <= n <= 64 for n in factor), 'factor')
    need(all(not n or lo >= 0 for n,(lo,hi) in zip(factor,bounds)), 'factor sign')
    p = restrict(p,bounds)
    need(all(all(n >= j for n,j in zip(k,factor)) for k in p), 'inexact factor')
    return {tuple(n-j for n,j in zip(k,factor)):x for k,x in p.items()}


def bernstein(p, bounds):
    degrees = [max((k[i] for k in p),default=0) for i in range(D)]
    if __import__('math').prod(n+1 for n in degrees) > 1000000:
        raise ResourceLimit('coefficient resource limit')
    power = {}
    for k,x in p.items():
        terms = {(0,)*D:x}
        for i,n in enumerate(k):
            lo,hi = bounds[i]
            next_terms = {}
            for key,c in terms.items():
                for j in range(n+1):
                    value = c*(comb(n,j)*lo**(n-j)*(hi-lo)**j)
                    if value != 0:
                        key2 = list(key)
                        key2[i] = j
                        key2 = tuple(key2)
                        next_terms[key2] = next_terms.get(key2,Q5())+value
            terms = next_terms
        power = add(power,terms)
    result = []
    for beta in product(*(range(n+1) for n in degrees)):
        value = Q5()
        for k,c in power.items():
            if all(a <= b for a,b in zip(k,beta)):
                for a,b,n in zip(k,beta,degrees):
                    c *= F(comb(b,a),comb(n,a))
                value += c
        result.append(value)
    return result


def prove(target, proof, bounds, assumptions):
    """Return strictness derived from rules; references can only point backward.

    Assumptions are reconstructed image constraints or interval bounds. They
    are never supplied as arbitrary certificate polynomials.
    """
    need(type(proof) is dict, 'proof object')
    if proof.get('op') == 'bernstein':
        fields(proof, ('op',))
        lower = min(bernstein(target,bounds))
        need(lower >= 0, 'negative Bernstein coefficient')
        return lower > 0
    if proof.get('op') in ('square','constant','interval'):
        if proof['op'] == 'interval':
            fields(proof,('op',))
            lo = Q5()
            for k,x in target.items():
                a,b = Q5(1),Q5(1)
                for n,(l,h) in zip(k,bounds):
                    ends = [l**n,h**n]
                    if n and n%2 == 0 and l <= 0 <= h:
                        ends.append(F(0))
                    choices = [q*r for q in (a,b) for r in (min(ends),max(ends))]
                    a,b = min(choices),max(choices)
                lo += min(a*x,b*x)
            need(lo >= 0, 'negative interval lower bound')
            return lo > 0
        return prove(target,{'op':'dag','nodes':[proof],'result':0},bounds,assumptions)
    fields(proof, ('op','nodes','result'))
    need(proof['op'] == 'dag' and type(proof['nodes']) is list, 'proof opcode')
    known = []
    for node in proof['nodes']:
        need(type(node) is dict, 'proof node object')
        op = node.get('op')
        if op == 'constant':
            fields(node, ('op','value'))
            x = decode(node['value'])
            need(x >= 0, 'negative constant')
            p,s = const(x),x > 0
        elif op == 'bernstein':
            fields(node, ('op','polynomial'))
            p = parse(node['polynomial'])
            lower = min(bernstein(p,bounds))
            need(lower >= 0, 'negative Bernstein coefficient')
            s = lower > 0
        elif op == 'square':
            fields(node, ('op','polynomial'))
            q = parse(node['polynomial'])
            p,s = mul(q,q),False
        elif op == 'domain':
            fields(node, ('op','index'))
            p,s = assumptions[index(node['index'],len(assumptions))],False
        elif op in ('add','multiply'):
            fields(node, ('op','args'))
            need(type(node['args']) is list and len(node['args']) >= 2, 'proof operands')
            rows = [known[index(i,len(known))] for i in node['args']]
            p,s = rows[0]
            for q,t in rows[1:]:
                p,s = (add(p,q),s or t) if op == 'add' else (mul(p,q),s and t)
        elif op in ('identity','substitute'):
            fields(node, ('op','source','polynomial'), ('values',))
            q,s = known[index(node['source'],len(known))]
            p = parse(node['polynomial'])
            if op == 'substitute':
                need('values' in node and type(node['values']) is list and len(node['values']) == D, 'substitution values')
                xs = [parse(x) for x in node['values']]
                for x,(lo,hi) in zip(xs,bounds):
                    need(min(bernstein(add(x,const(-lo)),bounds)) >= 0 and min(bernstein(add(const(hi),scale(x,-1)),bounds)) >= 0, 'substitution outside domain')
                q = substitute(q,xs)
                # Substitution must preserve every assumption used in the
                # source domain; an arbitrary change of image variables is
                # not a proof of the original image constraint.
                for g in assumptions:
                    need(min(bernstein(substitute(g,xs),bounds)) >= 0, 'substitution does not preserve assumptions')
            else:
                need('values' not in node, 'identity extra values')
            need(restrict(p,bounds) == restrict(q,bounds), 'polynomial identity')
        else:
            raise ValueError('unknown proof opcode')
        known.append((p,s))
    p,s = known[index(proof['result'],len(known))]
    need(restrict(p,bounds) == restrict(target,bounds), 'proof target identity')
    return s
