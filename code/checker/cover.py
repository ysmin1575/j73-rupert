"""Constructive closed covers; no area-only or coordinate-hull acceptance."""
from fractions import Fraction as F
from exact import need, fields, index, rational, bounds, decode, Q5
from geometry import rotation
from image import Grid, pose_image
from local import verify_leaf, point


def split_box(box,axis,cut):
    index(axis,5)
    lo,hi = box[axis]
    need(lo < cut < hi, 'noninterior split')
    a,b = list(box),list(box)
    a[axis],b[axis] = (lo,cut),(cut,hi)
    return a,b


def value(line,p):
    return line[0]+line[1]*p[0]+line[2]*p[1]


def clip(poly,line):
    """Closed clipping; tangent faces remain in their closed neighbour."""
    out = []
    for a,b in zip(poly,poly[1:]+poly[:1]):
        va,vb = value(line,a),value(line,b)
        if va >= 0:
            out.append(a)
        if va*vb < 0:
            t = va/(va-vb)
            out.append(tuple(x+t*(y-x) for x,y in zip(a,b)))
    return list(dict.fromkeys(out))


def canonical(poly):
    need(len(poly) >= 3, 'nondegenerate polygon')
    return min(tuple(poly[i:]+poly[:i]) for i in range(len(poly)))


def fan_partition(rect,walls,raw_polygons,raw_triangles):
    base = [(Q5(rect[0][0]),Q5(rect[1][0])),(Q5(rect[0][1]),Q5(rect[1][0])),(Q5(rect[0][1]),Q5(rect[1][1])),(Q5(rect[0][0]),Q5(rect[1][1]))]
    need(all(a < b for a,b in rect), 'rectangle width')
    polys = [base]
    for raw in walls:
        need(type(raw) is list and len(raw) == 3, 'wall shape')
        line = tuple(map(decode,raw))
        need(any(x != 0 for x in line), 'zero wall')
        new = []
        for poly in polys:
            vs = [value(line,p) for p in poly]
            if min(vs) < 0 < max(vs):
                new.extend((clip(poly,line),clip(poly,tuple(-x for x in line))))
            else:
                new.append(poly)
        polys = new
    declared = [[point(p) for p in poly] for poly in raw_polygons]
    need(len(declared) == len(polys) and sorted(map(canonical,declared)) == sorted(map(canonical,polys)), 'fan closed partition mismatch')
    expected = []
    for pi,poly in enumerate(declared):
        for k in range(1,len(poly)-1):
            expected.append((pi,canonical([poly[0],poly[k],poly[k+1]])))
    triangles = []
    observed = []
    for row in raw_triangles:
        fields(row,('polygon','vertices'))
        index(row['polygon'],len(declared))
        tri = [point(p) for p in row['vertices']]
        need(len(tri) == 3, 'triangle shape')
        a,b,c = tri
        need((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]) > 0, 'triangle area')
        observed.append((row['polygon'],canonical(tri)))
        triangles.append(row['vertices'])
    # Exact fan triangulation, including all edges and vertices. No area sum
    # can conceal an overlapping triangle or a missing boundary segment.
    need(sorted(observed) == sorted(expected), 'triangle cover mismatch')
    return triangles


def wire_box(bb):
    return [[str(a),str(b)] for a,b in bb]


def split_children(node,box,reason):
    children = node['children']
    need(type(children) is list and len(children) == 2, reason)
    return zip(children,split_box(box,node['axis'],rational(node['cut'])))


def local_tree(node,bb,context,residuals,path=()):
    need(type(node) is dict, 'tree object')
    if node.get('op') == 'split':
        fields(node,('op','axis','cut','children'))
        for side,(child,b) in enumerate(split_children(node,bb,'both closed children required')):
            local_tree(child,b,context,residuals,path+(side,))
    elif node.get('op') == 'residual':
        fields(node,('op',))
        residuals.append((context,bb,path))
    else:
        fields(node,('op','contacts','factor','multipliers','proof'))
        need(node['op'] == 'SC', 'local tree opcode')
        verify_leaf(dict(context,**node,bounds=wire_box(bb)))


def residual_lines(context,bb):
    tri = [point(p) for p in context['triangle']]
    a,b,c = tri
    bx,by,cx,cy = b[0]-a[0],b[1]-a[1],c[0]-a[0],c[1]-a[1]
    det = bx*cy-by*cx
    r = [(-a[0]*cy+a[1]*cx)/det,cy/det,-cx/det,0,0,0]
    t = [(-bx*a[1]+by*a[0])/det,-by/det,bx/det,0,0,0]
    one = [1,0,0,0,0,0]
    rest = [x-y for x,y in zip(one,r)]
    rho = [0]*6
    rho[3+context['dominant']] = context['sign']
    combine = lambda a,x,b,y: tuple(Q5.coerce(x*p+y*q) for p,q in zip(a,b))
    lines = [combine(r,1,one,-bb[0][0]),combine(one,bb[0][1],r,-1),combine(t,1,rest,-bb[1][0]),combine(rest,bb[1][1],t,-1),combine(rho,1,one,-bb[4][0]),combine(one,bb[4][1],rho,-1)]
    for j,k in enumerate(k for k in range(3) if k != context['dominant']):
        uk = [0]*6
        uk[k+3] = 1
        lines.extend((combine(uk,1,rho,-bb[j+2][0]),combine(rho,bb[j+2][1],uk,-1)))
    return lines


def direct_connection(node,box,contexts,lines,active):
    from exact import enclosure, Interval as I
    context = contexts[0]
    T = rotation(context['rotation'])
    anchor = tuple(map(decode,context['anchor']))
    s,u,_ = pose_image(box,T,context['label'],anchor,context['axis'])
    fields(node,('op','excluded'),('axis','cut','children'))
    left = set(active)
    need(type(node['excluded']) is list, 'exclusion rows')
    for row in node['excluded']:
        need(type(row) is list and len(row) == 2, 'exclusion pair')
        i,j = index(row[0],len(lines)),index(row[1],10)
        need(i in left, 'duplicate or inactive exclusion')
        upper = sum((enclosure(a)*x for a,x in zip(lines[i][j],[I(1),*s,*u])),I(0)).hi
        need(upper < 0, 'non-strict residual separation')
        left.remove(i)
    if node['op'] == 'connected':
        fields(node,('op','excluded'))
        need(not left, 'image reaches open residual')
    else:
        need(node['op'] == 'split', 'connection opcode')
        fields(node,('op','excluded','axis','cut','children'))
        for child,b in split_children(node,box,'both connection children'):
            direct_connection(child,b,contexts,lines,left)


def chart_cover(node,box):
    fields(node,('op','rotation','anchor','axis','label','original_box','radius','rectangle','walls','polygons','triangles','cells','constraints','direct'))
    need(bounds(node['original_box'],5) == box, 'original angular box binding')
    T = rotation(node['rotation'])
    axis = index(node['axis'],3)
    anchor = tuple(map(decode,node['anchor']))
    need(anchor == tuple(Q5(int(k == axis)) for k in range(3)), 'fan unit anchor')
    rect,radius = bounds(node['rectangle'],2),rational(node['radius'])
    need(radius > 0, 'positive cone radius')
    ss,uu,_ = pose_image(box,T,node['label'],anchor,axis)
    need(all(a <= x.lo <= x.hi <= b for (a,b),x in zip(rect,ss)), 'view image outside fan rectangle')
    need(all(-radius <= x.lo <= x.hi <= radius for x in uu), 'rotation image outside six-cone cube')
    triangles = fan_partition(rect,node['walls'],node['polygons'],node['triangles'])
    observed,residuals,contexts = set(),[],[]
    for cell in node['cells']:
        fields(cell,('triangle','dominant','sign','tree'))
        ti,dom = index(cell['triangle'],len(triangles)),index(cell['dominant'],3)
        need(type(cell['sign']) is int and cell['sign'] in (-1,1), 'cone sign')
        key = (ti,dom,cell['sign'])
        need(key not in observed, 'duplicate cone')
        observed.add(key)
        context = dict(op='SC',rotation=node['rotation'],anchor=node['anchor'],axis=axis,triangle=triangles[ti],dominant=dom,sign=cell['sign'],label=node['label'],original_box=node['original_box'],constraints={'data':node['constraints'],'rectangle':node['rectangle']} if node['constraints'] is not None else None)
        if context['constraints'] is None:
            context.update(label=None,original_box=None)
        contexts.append(context)
        bb = [(F(0),F(1))]*2+[(-F(1),F(1))]*2+[(F(0),radius)]
        local_tree(cell['tree'],bb,context,residuals)
    need(observed == {(i,d,s) for i in range(len(triangles)) for d in range(3) for s in (-1,1)}, 'missing cone chart')
    if residuals:
        need(node['direct'] is not None, 'unexcluded residual cells')
        lines = [residual_lines(c,b) for c,b,path in residuals]
        binding = dict(contexts[0],label=node['label'])
        direct_connection(node['direct'],box,[binding],lines,set(range(len(lines))))
    else:
        need(node['direct'] is None, 'unused direct connection')


def signed_cover(node,box):
    fields(node,('op','rotation','anchor','axis','label','original_box','mode'),('bounds','tree','view_bounds','radius','charts'))
    need(bounds(node['original_box'],5) == box, 'signed original box binding')
    T = rotation(node['rotation'])
    axis = index(node['axis'],3)
    need(type(node['anchor']) is list and len(node['anchor']) == 3, 'signed anchor')
    anchor = tuple(map(decode,node['anchor']))
    s,u,_ = pose_image(box,T,node['label'],anchor,axis)
    context = dict(op='SC',rotation=node['rotation'],anchor=node['anchor'],axis=axis,triangle=None,label=None,original_box=None,constraints=None)
    residuals = []
    common = ('op','rotation','anchor','axis','label','original_box','mode')
    if node['mode'] == 'box':
        fields(node,common+('bounds','tree'))
        bb = bounds(node['bounds'],5)
        need(all(a <= x.lo <= x.hi <= b for (a,b),x in zip(bb,s+u)), 'signed box misses actual image')
        local_tree(node['tree'],bb,dict(context,mode='box',dominant=None,sign=None),residuals)
    else:
        need(node['mode'] == 'cones', 'signed cover mode')
        fields(node,common+('view_bounds','radius','charts'))
        view = bounds(node['view_bounds'],2)
        r = rational(node['radius'])
        need(r > 0 and all(-r <= x.lo <= x.hi <= r for x in u), 'signed cone radius misses image')
        need(all(a <= x.lo <= x.hi <= b for (a,b),x in zip(view,s)), 'signed cone view misses image')
        observed = set()
        for chart in node['charts']:
            fields(chart,('dominant','sign','tree'))
            d = index(chart['dominant'],3)
            sign = chart['sign']
            need(type(sign) is int and sign in (-1,1) and (d,sign) not in observed, 'signed cone label')
            observed.add((d,sign))
            bb = view+[(-F(1),F(1))]*2+[(F(0),r)]
            local_tree(chart['tree'],bb,dict(context,mode='cone',dominant=d,sign=sign),residuals)
        need(observed == {(d,s) for d in range(3) for s in (-1,1)}, 'missing signed cone')
    need(not residuals, 'open signed cover')


def walk(node,box):
    need(type(node) is dict, 'cover node')
    op = node.get('op')
    if op == 'split':
        fields(node,('op','axis','cut','children'))
        for child,b in split_children(node,box,'missing cover child'):
            walk(child,b)
    elif op in ('G','tube'):
        fields(node,('op','box','vertex','direction') if op == 'G' else
               ('op','box','region','group_out','group_in','screen_lift'))
        need(bounds(node['box'],5) == box, op+' domain binding')
        verify_leaf(node)
    elif op == 'chart_cover':
        chart_cover(node,box)
    elif op == 'signed_cover':
        signed_cover(node,box)
    else:
        raise ValueError('open or unknown cover opcode')


def root(record,grid=None):
    fields(record,('root','box','tree'))
    grid = grid or Grid()
    k = index(record['root'],grid.count)
    b = bounds(record['box'],5)
    need(b == grid.rounded_box(k), 'original reduced-grid root binding')
    walk(record['tree'],b)
    return k
