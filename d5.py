#!/usr/bin/env python3

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

up, down = d.split('\n\n')

lines = [(x) for x in down.split('\n') if x]

print(lines)

# lines = [list(x) for x in d.split('\n') if x]
words = [x.split(',') for x in lines]

ints = [lmap(int, x) for x in words]

pairs = [tuple(map(int, x.split('|'))) for x in up.split('\n')]

print(pairs)
print(ints)


from itertools import zip_longest
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))

# m = {(r,c):char for r,row in enumerate(lines) for c, char in enumerate(row)}


from graphlib import TopologicalSorter

sda = 0
for row in ints:

    w = set()
    g = defaultdict(set)
    for a,b in pairs:
        if a in row and b in row:
            g[b].add(a)
            w.add(a)
            w.add(b)
    topo = TopologicalSorter(g)
    xx = (list(topo.static_order()))
    k = {x: i for i,x in enumerate(xx)}

    res = 0
    notok = defaultdict(list)

    orow = row

    notok.clear()

    ok = True
    for a,b in pairs:
        if a in orow and b in orow:
            if not (orow.index(a) < orow.index(b)):
                notok[tuple(orow)].append((a,b))

    assert len(set(orow)) == len(orow)

    if not notok:
        continue


    row.sort(key=lambda x: k[x])

    sda += (row[len(row) // 2])
print(sda)








