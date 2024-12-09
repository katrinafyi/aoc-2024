#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [list(x) for x in d.split('\n') if x]

# print(lines)

# print(ints)

from itertools import combinations, zip_longest
from functools import lru_cache
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))
def ints(line: str):
  line = ''.join(c if c.isdigit() else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [list(x) for x in d.split('\n') if x]
m = {(r,c):char for r,row in enumerate(lines) for c, char in enumerate(row)}
print(m)

ants = defaultdict(set)
for (r,c),ant in m.items():
  if ant != '.':
    ants[ant].add((r,c))

addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)

antis = set()
for ant, poses in ants.items():
  for pos1,pos2 in combinations(poses, r=2):
    d = subb(pos1, pos2)
    for i in range(500):
      a1 = addd(pos1, mull(i, d))
      a2 = subb(pos2, mull(i, d))
      antis.add(tuple(a2))
      antis.add(tuple(a1))
print(len(antis & set(m.keys())))




dirs = [(-1,0), (0,-1), (1,0), (0,1)]
dirs.reverse()
right = lambda asd: dirs[(dirs.index(asd) + 1) % len(dirs)]

rows = []
for l in lines:
  target, rest = l.split(':')
  target = int(target)
  rest = [int(x) for x in rest.split()]
  rows.append((target, rest))

def check(target, x, nums):
  if not nums:
    return x == target
  y, *nums = nums
  return check(target, x+y, nums) or check(target, x*y, nums) or check(target, int(str(x) + str(y)), nums)

y = 0
for target, xs in rows:
  x, *xs = xs
  if check(target, x, xs):
    y += target

print(y)
