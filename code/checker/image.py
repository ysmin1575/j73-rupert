"""Rational Taylor enclosures, canonical grid, and original-angle pullback."""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from exact import Interval as I, need, fields, index, bounds, enclosure, Q5
from geometry import Geometry, mv, mm, transpose, identity
import polynomial as P


@lru_cache(maxsize=4096)
def scalar_trig(x):
    need(abs(x) <= 8, 'angle outside Taylor range')
    # Lagrange remainder for degree 159/158; derivatives of sin/cos <= 1.
    ss = sum(((-1)**k*x**(2*k+1)/factorial(2*k+1) for k in range(80)),F(0))
    cc = sum(((-1)**k*x**(2*k)/factorial(2*k) for k in range(80)),F(0))
    es,ec = abs(x)**160/factorial(160),abs(x)**159/factorial(159)
    return I(ss-es,ss+es),I(cc-ec,cc+ec)


def trig(x):
    x = I.coerce(x)
    c,h = (x.lo+x.hi)/2,(x.hi-x.lo)/2
    s,t = scalar_trig(c)
    if not h:
        return s,t
    delta,rem = I(-h,h),I(-h*h/2,h*h/2)
    rough_s,rough_c = s+t*delta+rem,t-s*delta+rem
    sl,cl = scalar_trig(x.lo)
    sr,cr = scalar_trig(x.hi)
    def extrema(left,right,rough,derivative):
        if derivative.lo >= 0 or derivative.hi <= 0:
            return I(min(left.lo,right.lo),max(left.hi,right.hi))
        # Critical points are separated by pi>1. In this short interval a
        # positive extremum is +1 and a negative extremum is -1.
        if 2*h < 1 and rough.lo > 0:
            return I(min(left.lo,right.lo),1)
        if 2*h < 1 and rough.hi < 0:
            return I(-1,max(left.hi,right.hi))
        return I(-1,1)
    return extrema(sl,sr,rough_s,rough_c),extrema(cl,cr,rough_c,-rough_s)


def frame(t,p):
    st,ct = trig(t)
    sp,cp = trig(p)
    return ((-st,ct,I(0)),(-ct*cp,-st*cp,sp),(ct*sp,st*sp,cp))


def derivatives(t,p):
    st,ct = trig(t)
    sp,cp = trig(p)
    return ((-ct,-st,I(0)),(st*cp,-ct*cp,I(0))),((I(0),I(0),I(0)),(ct*sp,st*sp,cp))


def screen(a):
    s,c = trig(a)
    return ((c,-s,I(0)),(s,c,I(0)),(I(0),I(0),I(1)))


@lru_cache(maxsize=1)
class Grid:
    shape = (12,17,12,17,30)
    count = 1248480
    pi_lo = F(314159265358979323846264338327950288419716939937510,10**50)
    pi_hi = pi_lo+F(1,10**50)

    def __init__(self):
        def atan(q):
            a = sum(((-1)**k*q**(2*k+1)/F(2*k+1) for k in range(80)),F(0))
            return a,a+q**161/161
        a,b = atan(F(1,5)),atan(F(1,239))
        need(self.pi_lo < 16*a[0]-4*b[1] < 16*a[1]-4*b[0] < self.pi_hi, 'Machin pi enclosure')
        self.domain = ((0,2*self.pi_hi/5),(0,self.pi_hi/2),(0,2*self.pi_hi/5),(0,self.pi_hi/2),(-self.pi_hi/2,self.pi_hi/2))

    def box(self,k):
        index(k,self.count)
        coords = []
        for n in reversed(self.shape):
            k,r = divmod(k,n)
            coords.append(r)
        return [(F(a)+(b-a)*i/n,F(a)+(b-a)*(i+1)/n) for (a,b),i,n in zip(self.domain,reversed(coords),self.shape)]

    def rounded_box(self,k):
        return [(binary64(a,False),binary64(b,True)) for a,b in self.box(k)]


def binary64(x,up):
    """Directed finite binary64 replay, including subnormals; exact integers.

    Only rational values within the largest finite binary64 are supported.
    Grid replay stays in this range; overflow is rejected, never approximated.
    """
    need(abs(x) <= (2**53-1)*2**971, 'binary64 finite replay range')
    if x == 0:
        return F(0)
    if x < 0:
        return -binary64(-x,not up)
    e = x.numerator.bit_length()-x.denominator.bit_length()
    power = lambda k: F(2**k) if k >= 0 else F(1,2**(-k))
    if x < power(e):
        e -= 1
    step = power(max(e-52,-1074))
    y = x/step
    n = y.numerator//y.denominator
    return (n+int(up and y != n))*step


def nearest64(x):
    a,b = binary64(x,False),binary64(x,True)
    if x-a != b-x:
        return a if x-a < b-x else b
    if a == b:
        return a
    return a if (a/(b-a)).numerator%2 == 0 else b


def first_sweep_box(root,path):
    need(type(path) is str and (path == '' or path.startswith('/')), 'first sweep path')
    bb = Grid().rounded_box(root)
    for token in path.split('/')[1:]:
        need(token.isascii() and token.isdecimal() and str(int(token)) == token, 'canonical child path')
        mids = [nearest64(nearest64(a+b)/2) for a,b in bb]
        widths = [nearest64(b-a) for a,b in bb]
        threshold = nearest64(F(5404319552844595,9007199254740992)*max(widths))
        dims = [i for i in range(5) if widths[i] >= threshold and bb[i][0] < mids[i] < bb[i][1]]
        child = index(int(token),2**len(dims))
        for j,k in enumerate(dims):
            bb[k] = (mids[k],bb[k][1]) if child & (1 << (len(dims)-1-j)) else (bb[k][0],mids[k])
    return bb


def label(raw):
    fields(raw,('group_out','group_in','screen_lift','view_sign'))
    go,gi = index(raw['group_out'],10),index(raw['group_in'],10)
    need(type(raw['screen_lift']) is str and raw['screen_lift'] in ('I','rho_pi'), 'screen lift')
    need(type(raw['view_sign']) is int and raw['view_sign'] in (-1,1), 'view sign')
    return go,gi


def pose_image(box,T,lab,anchor,axis):
    g = Geometry()
    go,gi = label(lab)
    index(axis,3)
    need(len(anchor) == 3 and anchor[axis] != 0, 'view anchor')
    qmat = lambda m: tuple(tuple(enclosure(x) for x in r) for r in m)
    b = [I(a,z) for a,z in box]
    O = mm(frame(b[2],b[3]),g.align)
    inner = mm(mm(screen(b[4]),frame(b[0],b[1])),g.align)
    signs = (1,1,1) if lab['screen_lift'] == 'I' else (-1,-1,1)
    LO = tuple(tuple(s*x for x in row) for s,row in zip(signs,O))
    E = mm(mm(mm(qmat(transpose(g.groups[go])),mm(transpose(LO),inner)),qmat(g.groups[gi])),qmat(transpose(T)))
    if lab['screen_lift'] == 'I' and box[0][0] == box[0][1] == box[2][0] == box[2][1] and box[1][0] == box[1][1] == box[3][0] == box[3][1] and box[4] == (0,0):
        E = qmat(mm(mm(transpose(g.groups[go]),g.groups[gi]),transpose(T)))
    den = 1+sum(E[k][k] for k in range(3))
    need(den.lo > 0, 'Cayley denominator not positive')
    u = [(E[(k+2)%3][(k+1)%3]-E[(k+1)%3][(k+2)%3])/den for k in range(3)]
    w = mv(qmat(transpose(g.groups[go])),O[2])
    wk = w[axis]
    need(wk.lo > 0 or wk.hi < 0, 'view denominator crosses zero')
    s = [enclosure(anchor[axis])*w[k]/wk-enclosure(anchor[k]) for k in range(3) if k != axis]
    if box[3] == (0,0):
        pole = mv(transpose(g.groups[go]),g.pole)
        if pole[axis] != 0:
            s = [enclosure(anchor[axis]*pole[k]/pole[axis]-anchor[k]) for k in range(3) if k != axis]
    return s,u,1 if wk.lo > 0 else -1


def constraints(raw,box,T,lab,anchor,axis,rect,w,u):
    if raw is None:
        return []
    fields(raw,('schema','alpha_product_interval','cayley_intervals','chart_sign','outer_polar_sine_interval','identity','outer_cosine_squared_interval'))
    need(raw['schema'] == 'j73-original-angle-constraints-v3', 'pre-v3 or unknown constraints')
    need(raw['identity'] == '-sigma*lift0*((d0 cross Go*w).Go*Cnum(u)*T*Gi^T*d0) = D2*norm(w)*sin(po)*sin(pi)*sin(alpha)*(1+u2)', 'v3 identity label')
    need(type(raw['cayley_intervals']) is list and len(raw['cayley_intervals']) == 3, 'Cayley interval count')
    need(anchor == tuple(Q5(int(i == axis)) for i in range(3)), 'correlation requires unit anchor')
    ss,uu,sign = pose_image(box,T,lab,anchor,axis)
    need(all(a <= x.lo <= x.hi <= b for (a,b),x in zip(rect,ss)), 'correlation rectangle misses original image')
    need(type(raw['chart_sign']) is int and raw['chart_sign'] == sign, 'chart sign')
    norm = (I(1)+sum((I(a,b).square() for a,b in rect),I(0))).sqrt()
    sins = [trig(I(*box[k]))[0] for k in (3,1,4)]
    phi = Q5(F(1,2),F(1,2))
    prod = enclosure(phi*phi+1)*norm*sins[0]*sins[1]*sins[2]
    co = trig(I(*box[3]))[1].square()
    intervals = bounds([raw['alpha_product_interval'],*raw['cayley_intervals'],raw['outer_polar_sine_interval'],raw['outer_cosine_squared_interval']],6)
    for j,((a,b),x) in enumerate(zip(intervals,[prod,*uu,sins[0],co])):
        need(a <= x.lo <= x.hi <= b, 'unproved image interval '+str(j))
    g = Geometry()
    go,gi = label(lab)
    aa = [P.const(x) for x in mv(T,mv(transpose(g.groups[gi]),g.pole))]
    u2 = P.dot(u,u)
    D = P.add(P.const(1),u2)
    au = P.dot(u,aa)
    cu = P.cross(u,aa)
    rot = [P.add(P.mul(P.add(P.const(1),P.scale(u2,-1)),aa[k]),P.scale(P.mul(u[k],au),2),P.scale(cu[k],2)) for k in range(3)]
    pmv = lambda M,x: [P.add(*(P.scale(z,a) for z,a in zip(x,row))) for row in M]
    f = P.dot(P.cross([P.const(x) for x in g.pole],pmv(g.groups[go],w)),pmv(g.groups[go],rot))
    f = P.scale(f,-sign*(1 if lab['screen_lift'] == 'I' else -1))
    lo,hi = intervals[0]
    gps = [P.add(f,P.scale(D,-lo)),P.add(P.scale(D,hi),P.scale(f,-1))]
    for x,(lo,hi) in zip(u,intervals[1:4]):
        gps.extend((P.add(x,P.const(-lo)),P.add(P.const(hi),P.scale(x,-1))))
    x = P.dot([P.const(z) for z in g.pole],pmv(g.groups[go],w))
    xx,ww = P.mul(x,x),P.scale(P.dot(w,w),sum(z*z for z in g.pole))
    lo,hi = intervals[-1]
    gps.extend((P.add(xx,P.scale(ww,-lo)),P.add(P.scale(ww,hi),P.scale(xx,-1))))
    return gps
