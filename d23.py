#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

# /// script
# dependencies = [
# ]
# ///


import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict, Counter, deque
from pprint import pprint

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))

# print(lines)

# print(ints)

from itertools import combinations, permutations, zip_longest
from functools import cache, lru_cache, reduce
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))

def concat(xss):
  return [x for xs in xss for x in xs]

addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)
dirs = [(-1,0), (0,-1), (1,0), (0,1)] # (r,c), turning left, starting from UP
left = lambda asd: dirs[(dirs.index(asd) + 1) % len(dirs)]
right = lambda asd: dirs[(dirs.index(asd) - 1) % len(dirs)]
dirs8 = concat([d, addd(d,left(d))] for d in dirs)
left8 = lambda asd: dirs8[(dirs8.index(asd) + 1) % len(dirs8)]

import sys
def ints(line: str):
  line = ''.join(c if c.isdigit() or c == '-' else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

#
lines = [(x.strip()) for x in d.split('\n') if x]
#
# m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}
#
movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

# poses = list(tuple(ints(x)) for x in d.split('\n') if x)
# print(poses)


# clear = {k for k,v in m.items() if v in '.SE'}
# start = next(k for k,v in m.items() if v == 'S')
# end = next(k for k,v in m.items() if v == 'E')
#
# print(clear, start, end)

import heapq

def dist(p1, p2):
  x,y = subb(p1,p2)
  return abs(x) + abs(y)


pairs = [x.split('-') for x in lines]
print(pairs)

conns = defaultdict(set)
for a,b in pairs:
  conns[a].add(a)
  conns[b].add(b)
  conns[a].add(b)
  conns[b].add(a)

seen = set()
threes = set()
asd = 0
print(conns)

larg = []
for comp in conns:

  n = len(conns[comp])
  while n > len(larg):
    for nset in combinations(conns[comp], n):
      if all(x in conns[y] for y in nset for x in nset):
        if len(nset) > len(larg):
          larg = list(sorted(nset))
    n -= 1

  for three in map(frozenset,combinations(conns[comp], 3)):
    if three in threes: continue
    threes.add(three)
    if all(x in conns[y] for y in three for x in three):
      if any(x.startswith('t') for x in three):
        # print(three)
        asd += 1
print(asd)

print(','.join(larg))
