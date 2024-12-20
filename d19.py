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

up, down = d.split('\n\n')

avail = up.replace(',', '').strip().split()

wanted = down.strip().split()

print(avail)
# print(wanted)

print(len(avail))

import re

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
print('max', max(w.count(av) for w in wanted for av in avail))
# for w in wanted:
#   for av in avail:
#     print(w.count(av))
#     # assert w.count(av) in {0,1}

# avail.sort(key=len)

@cache
def go(want: str):
  # print('go', want, len(avail))
  # ret = 0
  if not want: return 1
  # if want in avail:
  #   ret += 1
  # if not avail:
  #   return 0

  ret = 0
  for av in avail:
    if want.startswith(av):
      ret += go(want[len(av):])
  return ret

  av = avail[0]
  if av not in want:
    return go(want, avail[1:])

  ret = 0
  l, r = want.split(av, 1)
  ret += go(l, avail[1:]) * go(r, avail)  # yes split
  ret += go(l +  + r)  # do not split
  return ret

x = 0
print(go('brwrr'))
# print(go(wanted[0]))
for i, w in enumerate(wanted):
  # print(i, len(wanted), w, go(w, tuple(avail)))
  x += go(w)
  # if go(w):
  #   print(w, 'oka')
  #   x += 1
  # else:
  #   print(w, 'not')
#
print(x)

