#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))

# print(lines)

# print(ints)

from itertools import combinations, zip_longest
from functools import lru_cache
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))
def ints(line: str):
  line = ''.join(c if c.isdigit() else ' ' for c in line)
  return [int(x) for x in line.split() if x]

def concat(xss):
  return [x for xs in xss for x in xs]

addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)
dirs = [(-1,0), (0,-1), (1,0), (0,1)] # (r,c), turning left, starting from UP
left = lambda asd: dirs[(dirs.index(asd) + 1) % len(dirs)]
dirs8 = concat([d, addd(d,left(d))] for d in dirs)

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [(x) for x in d.split('\n') if x]

# m = {(r,c):int(char) if char != '.' else 1000 for r,row in enumerate(lines) for c, char in enumerate(row)}

# print(m)

d = defaultdict(int)
for n in ints(lines[0]):
  d[n] += 1

for i in range(75):
  new = defaultdict(int)
  for n, count in d.items():
    if n == 0:
      new[1] += count
    elif len(str(n)) % 2 == 0:
      new[int(str(n)[:len(str(n))//2])] += count
      new[int(str(n)[len(str(n))//2:])] += count
    else:
      new[n*2024] += count

    d = new
print(sum(d.values()))

