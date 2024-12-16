#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

# /// script
# dependencies = [
#   "scipy",
# ]
# ///

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict, Counter
from collections import deque
import math

from fractions import Fraction
import heapq

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))

# print(lines)

# print(ints)

from itertools import combinations, zip_longest
from functools import lru_cache, reduce, cache
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))
def ints(line: str):
  line = ''.join(c if c.isdigit() or c == '-' else ' ' for c in line)
  return [int(x) for x in line.split() if x]

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

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

lines = [list(x.strip()) for x in d.split('\n') if x]

m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}

movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

clear = {k for k,v in m.items() if v in '.SE'}

start = next(iter(k for k,v in m.items() if v == 'S'))
startd = movemap['>']
end = next(iter(k for k,v in m.items() if v == 'E'))

paths = []
q = []
q.append((0,0,start,movemap['>'],{start}))
firstseenat = {}
howmanytimes = {}
minw = None

@cache
def heuristic():
  q = []
  for d in dirs:
    q.append((0,0,end,d,None))
  firstseenat = {}
  minw = None
  while q:
    _, w,pos,dir,path = heapq.heappop(q)
    assert pos in clear
    # if (pos,dir) == (start,startd) and minw is None: minw = w
    # if minw is not None and w > minw: break
    if (pos,dir) in firstseenat: continue
    firstseenat[pos,dir] = w
    for d in dirs:
      if d == mull(-1,dir): continue # no turning back
      pos2 = addd(d, pos)

      cost = 1 if d == dir else 1000
      if cost == 1 and pos2 in clear:
        heapq.heappush(q, (0, w+cost,pos2,d,None))
      else:
        heapq.heappush(q, (0, w+cost,pos,d,None))
  return lambda pos,d: firstseenat[pos,d]

while q:
  _, w,pos,dir,path = heapq.heappop(q)
  if pos == end:
    if minw is None:
      minw = w
    if w == minw:
      paths.append(path)
    continue
  # if pos in firstseenat:
  #   continue
  if minw is not None and w > minw: break

  if pos not in firstseenat:
    firstseenat[pos] = w

  for d in dirs:
    if d == mull(-1,dir): continue # no turning back
    pos2 = addd(d, pos)
    cost = 1 if d == dir else 1001
    if pos2 in clear:
      heapq.heappush(q, (w+cost+heuristic()(pos2,d), w+cost,pos2,d,path | {pos2}))

print()
print(minw)
print(len(set(x for path in paths for x in path)))
