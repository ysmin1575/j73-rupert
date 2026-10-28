"""Strict wire numbers and outward dyadic intervals. No floating arithmetic."""
import json
from dataclasses import dataclass
from fractions import Fraction as F
from functools import total_ordering
from math import isqrt


class ResourceLimit(RuntimeError):
    """Verification stopped before a mathematical decision was reached."""


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def fields(obj, required, optional=()):
    need(type(obj) is dict, 'object required')
    need(set(required) <= obj.keys() <= set(required) | set(optional), 'missing or unknown fields')


def index(x, n):
    need(type(x) is int and 0 <= x < n, 'index type or range')
    return x


def rational(raw):
    if type(raw) is int:
        return F(raw)
    need(type(raw) is str, 'integer or canonical rational required')
    try:
        q = F(raw)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rational') from None
    need(str(q) == raw, 'noncanonical rational')
    return q


def loads(raw):
    def pairs(xs):
        result = {}
        for k, v in xs:
            need(k not in result, 'duplicate JSON key: '+k)
            result[k] = v
        return result
    def reject(_):
        raise ValueError('floating or nonfinite JSON number')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)


@total_ordering
@dataclass(frozen=True, eq=False)
class Q5:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        need(type(self.a) in (int, F) and type(self.b) in (int, F), 'exact coefficients')
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    @staticmethod
    def coerce(x):
        return x if type(x) is Q5 else Q5(x)

    def __add__(self, x):
        x = self.coerce(x)
        return Q5(self.a+x.a, self.b+x.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, x):
        return self + -self.coerce(x)

    def __rsub__(self, x):
        return self.coerce(x) + -self

    def __mul__(self, x):
        x = self.coerce(x)
        return Q5(self.a*x.a+5*self.b*x.b, self.a*x.b+self.b*x.a)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.coerce(x)
        norm = x.a*x.a-5*x.b*x.b
        need(norm != 0, 'zero divisor')
        return self*Q5(x.a/norm, -x.b/norm)

    def __pow__(self, n):
        need(type(n) is int and n >= 0, 'exponent')
        result = Q5(1)
        for _ in range(n):
            result *= self
        return result

    def sign(self):
        a, b = self.a, self.b
        if not b:
            return (a > 0)-(a < 0)
        if not a or (a > 0) == (b > 0):
            return (b > 0)-(b < 0)
        return ((a > 0)-(a < 0))*((a*a > 5*b*b)-(a*a < 5*b*b))

    def __eq__(self, x):
        if type(x) not in (Q5, int, F):
            return False
        x = self.coerce(x)
        return self.a == x.a and self.b == x.b

    def __lt__(self, x):
        return (self-x).sign() < 0

    def __hash__(self):
        return hash(self.a) if self.b == 0 else hash((self.a, self.b))


def decode(raw):
    if type(raw) is list:
        need(len(raw) == 2, 'Q5 pair')
        return Q5(*(rational(x) for x in raw))
    return Q5(rational(raw))


def bounds(raw, dimension):
    need(type(raw) is list and len(raw) == dimension, 'bounds dimension')
    need(all(type(p) is list and len(p) == 2 for p in raw), 'endpoint pair')
    result = [tuple(rational(x) for x in p) for p in raw]
    need(all(a <= b for a, b in result), 'reversed interval')
    return result


BITS = 320
UNIT = 1 << BITS


def floor(q):
    return F(q.numerator*UNIT//q.denominator, UNIT)


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F = None

    def __post_init__(self):
        a = F(self.lo)
        b = a if self.hi is None else F(self.hi)
        need(a <= b, 'reversed interval')
        object.__setattr__(self, 'lo', floor(a))
        object.__setattr__(self, 'hi', -floor(-b))

    @staticmethod
    def coerce(x):
        return x if type(x) is Interval else Interval(x)

    def __add__(self, x):
        x = self.coerce(x)
        return Interval(self.lo+x.lo, self.hi+x.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, x):
        return self+-self.coerce(x)

    def __rsub__(self, x):
        return self.coerce(x)+-self

    def __mul__(self, x):
        x = self.coerce(x)
        values = [a*b for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.coerce(x)
        need(x.lo > 0 or x.hi < 0, 'denominator includes zero')
        return self*Interval(1/x.hi, 1/x.lo)

    def square(self):
        return Interval(0 if self.lo <= 0 <= self.hi else min(self.lo**2,self.hi**2),
                        max(self.lo**2,self.hi**2))

    def sqrt(self):
        need(self.lo >= 0, 'negative square root')
        a = isqrt(self.lo.numerator*UNIT*UNIT//self.lo.denominator)
        b = isqrt(self.hi.numerator*UNIT*UNIT//self.hi.denominator)
        return Interval(F(a,UNIT), F(b if F(b,UNIT)**2 == self.hi else b+1,UNIT))

    def absolute(self):
        return Interval(0 if self.lo <= 0 <= self.hi else min(abs(self.lo),abs(self.hi)),
                        max(abs(self.lo),abs(self.hi)))


def enclosure(x):
    x = Q5.coerce(x)
    return Interval(x.a)+Interval(x.b)*Interval(5).sqrt()
