#!/usr/bin/env python3

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

# up, down = d.split('\n\n')

lines = [list(x) for x in d.split('\n') if x]

print(lines)

# lines = [list(x) for x in d.split('\n') if x]
# words = [x.split(',') for x in lines]

# ints = [lmap(int, x) for x in words]

# pairs = [tuple(map(int, x.split('|'))) for x in up.split('\n')]

print(lines)
# print(ints)


from itertools import zip_longest
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))

m = {(r,c):char for r,row in enumerate(lines) for c, char in enumerate(row)}
print(m)

dirs = [(-1,0), (0,-1), (1,0), (0,1)]
dirs.reverse()
right = lambda asd: dirs[(dirs.index(asd) + 1) % len(dirs)]

g = next(iter(k for k in m if m[k] == '^'))

om = m

def go(b=None):
    pos = g
    d = (-1,0)
    seen = defaultdict(list)
    seenorder = []
    seenset = set()
    crashed = set()
    asd = 0
    exited = False
    while True:
        seen[pos, d].append(len(seen))
        seenorder.append((pos,d))
        pos2 = (pos[0] + d[0], pos[1] + d[1])
        while m.get(pos2) == '#' or pos2 == b:
            crashed.add(pos2)
            d = right(d)
            pos2 = (pos[0] + d[0], pos[1] + d[1])
        pos2 = (pos[0] + d[0], pos[1] + d[1])
        pos = pos2
        if pos not in m:
            exited = True
            break
        if (pos,d) in seen:
            break
    # candidates = {x for x,_ in seen}
    # print(candidates)
    return exited, {x for x,_ in seen}

fdsa = go()[1]

asdf = 0
for b in fdsa:
    exited,_ = go(b)
    if not exited:
        asdf += 1
print('asd', asdf)

