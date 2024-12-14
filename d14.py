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
from functools import lru_cache, reduce
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
lines = [(x) for x in d.split('\n') if x]

# m = {(r,c):(char) if char != '.' else None for r,row in enumerate(lines) for c, char in enumerate(row)}

# from scipy.optimize import linprog
import math

from fractions import Fraction

lines = (lmap(ints, lines))

bots = []
for bot in lines:
  pos = bot[0], bot[1]
  v = bot[2], bot[3]
  bots.append([pos,v])

XSIZE = 101
YSIZE = 103
# XSIZE = 11
# YSIZE = 7

import os, time
start = 0
for i, (pos,v) in  enumerate(bots):
  bots[i][0] = list(addd(bots[i][0], mull(start, v)))
  bots[i][0][0] %= XSIZE
  bots[i][0][1] %= YSIZE
for i in range(10000):
  j = i
  poses = set()
  for i, (pos,v) in  enumerate(bots):
    bots[i][0] = list(addd(bots[i][0], v))
    bots[i][0][0] %= XSIZE
    bots[i][0][1] %= YSIZE
    poses.add(tuple(bots[i][0]))

  numadj = 0
  for pos,_ in bots:
    for d in dirs:
      if addd(d, pos) in poses:
        numadj += 1

  if numadj > 500:
    # os.system('clear', )
    for r in range(XSIZE):
      for c in range(YSIZE):
        if (r,c) in poses:
          print('#', end='')
        else:
          print(' ', end='')
      print()
    print(flush=True)
    print(start+j+1, numadj, flush=True)
    time.sleep(10*1/60)

quadrants = defaultdict(int)
for (r,c),v in bots:
  if r == (XSIZE-1)//2:
    qr = None
  elif r > (XSIZE-1)//2:
    qr = 1
  else: qr = 0

  if c == (YSIZE-1)//2:
    qc = None
  elif c > (YSIZE-1)//2:
    qc = 1
  else: qc = 0

  quadrants[qr,qc] += 1

print(quadrants)
print(reduce(lambda x,y: x*y, (v for k,v in quadrants.items() if None not in k)))








