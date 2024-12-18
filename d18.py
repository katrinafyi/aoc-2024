#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

# /// script
# dependencies = [
# ]
# ///


import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict, Counter, deque

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))

# print(lines)

# print(ints)

from itertools import combinations, zip_longest
from functools import lru_cache, reduce
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
# lines = [list(x.strip()) for x in d.split('\n') if x]
#
# m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}
#
movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

poses = list(tuple(ints(x)) for x in d.split('\n') if x)
# print(poses)

def go(included: int):
  bound = 71
  # bound = 7
  clear = {(r,c) for r in range(bound) for c in range(bound)}
  for p in poses[:included]:
    clear.remove(p)

  pos = (0,0)
  q = deque()
  q.append((pos,0))
  seen = set()
  end = (bound-1, bound-1)
  while q:
    pos,l = q.popleft()
    if pos in seen: continue
    if pos == end:
      print(l)
      return True
    seen.add(pos)
    for d in dirs:
      pos2 = addd(d, pos)
      if pos2 in clear and pos2 not in seen:
        q.append((pos2,l+1))
  return False

for i in reversed(range(len(poses))):
  print(i, poses[i], len(poses))
  if go(i):
    print(poses[i])
    break

