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

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [list(x) for x in d.split('\n') if x]

addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)



m = {(r,c):int(char) if char != '.' else 1000 for r,row in enumerate(lines) for c, char in enumerate(row)}

# print(m)

dirs = [(-1,0), (0,-1), (1,0), (0,1)]
prevok = {k: 1 for k,v in m.items() if v == 9}
prevuniq = {k: {k} for k in prevok}
for startinglevel in reversed(range(9)):
  nextok = defaultdict(int)
  nextuniq = defaultdict(set)
  for pos, n in prevok.items():
    for dir in dirs:
      if m.get(addd(pos, dir)) == startinglevel:
        nextok[addd(pos,dir)] += n
        nextuniq[addd(pos,dir)] |= prevuniq[pos]
  prevok = nextok
  prevuniq = nextuniq

print(sum(map(len,prevuniq.values())))
print(sum(prevok.values()))




#
