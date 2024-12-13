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
right = lambda asd: dirs[(dirs.index(asd) - 1) % len(dirs)]
dirs8 = concat([d, addd(d,left(d))] for d in dirs)
left8 = lambda asd: dirs8[(dirs8.index(asd) + 1) % len(dirs8)]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
# lines = [list(x) for x in d.split('\n') if x]

# m = {(r,c):(char) if char != '.' else None for r,row in enumerate(lines) for c, char in enumerate(row)}

from scipy.optimize import linprog
import math

from fractions import Fraction

chunks = d.split('\n\n')
asd = 0
for c in chunks:
  ax,ay,bx,by,px,py = lmap(Fraction, ints(c.replace('\n', ' ')))
  px += 10000000000000
  py += 10000000000000

  b = (px*ay - ax*py)  / ((- ax*by) + bx*ay)
  a = (py - b*by) / ay

  # a*ax + b*bx = px
  # a*ay + b*by = py
  # a = (py - b*by) / ay
  # ((py - b*by) / ay)*ax + b*bx = px
  # ((ax*py - ax*b*by) / ay)+ b*bx = px
  # (ax*py - ax*b*by) + b*bx*ay = px*ay
  # (- ax*b*by) + b*bx*ay = px*ay - ax*py 
  # b = (px*ay - ax*py) / ((- ax*by) + bx*ay)

  #
  # costs.sort()
  # if costs:
  #   asd += costs[0][0]
  # if res.success:
  #   print(lmap(int,res.x))
  #   asd += round(res.fun)
  if a.denominator == 1 == b.denominator:
    if a*ax + b*bx == px and a*ay + b*by == py:
      asd += 3*a + b
print(asd)
