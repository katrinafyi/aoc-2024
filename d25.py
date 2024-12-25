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
def dist(p1, p2): return sum(map(abs, subb(p1,p2)))

import sys
import heapq
def ints(line: str):
  line = ''.join(c if c.isdigit() or c == '-' else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

#
#
#
movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

# clear = {k for k,v in m.items() if v in '.SE'}
# start = next(k for k,v in m.items() if v == 'S')
# end = next(k for k,v in m.items() if v == 'E')
#
# print(clear, start, end)

chunks = d.split('\n\n')

locks = []
keys = []
for d in chunks:

  lines = [list(x.strip()) for x in d.split('\n') if x]
  islock = '#' in lines[0]
  transpose = lambda x: list(map(list, zip_longest(*x, fillvalue='.')))
  print(islock)
  lines = transpose(lines)
  if islock:
    locks.append([l.count('#') for l in lines])
  else:
    keys.append([l.count('#') for l in lines])
  # m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}
  print()

asd = 0
print(len(locks))
print(len(keys))
for lock in locks:
  for key in keys:
    print(lock, key)
    assert len(lock) == len(key)
    oko = all((l+k)<=7 for l,k in zip(lock,key))
    asd += oko
print(asd)
