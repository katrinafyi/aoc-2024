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


numpad = tuple({
  (0,0): '7',
  (0,1): '8',
  (0,2): '9',

  (1,0): '4',
  (1,1): '5',
  (1,2): '6',

  (2,0): '1',
  (2,1): '2',
  (2,2): '3',


  # (3,0): '9',
  (3,1): '0',
  (3,2): 'A',
}.items())

dirpad = tuple({
  # (0,0): ''
  (0,1): '^',
  (0,2): 'A',

  (1,0): '<',
  (1,1): 'v',
  (1,2): '>',
}.items())


def dist(p1, p2):
  x,y = subb(p1,p2)
  return abs(x) + abs(y)

# @cache
import random
def go(pad, old: str, new: str):
  pad = dict(pad)
  def find(c):
    return next(k for k,v in pad.items() if v == c)
  pos = find(old)
  cpos = find(new)
  # possible = []
  # for c in target:
  #   opos = pos
  #   cpos = find(c)
  poss = []
  if 1:
    opos = pos
    dr,dc = 0,0
    thismove = []
    while cpos != pos:
      dr, dc = subb(cpos, pos)
      mov = 'v' if dr > 0 else '^'
      if dr != 0 and random.random() > 0.5 and addd(movemap[mov], pos) in pad:
        thismove.append(mov)
        pos = addd(movemap[mov], pos)
        continue
      mov = '>' if dc > 0 else '<'
      if dc != 0 and random.random() > 0.5 and addd(movemap[mov], pos) in pad:
        thismove.append(mov)
        pos = addd(movemap[mov], pos)
        continue
      # assert (pos == cpos)
      # assert (dr,dc) == (0,0)

    return [tuple(thismove) + ('A', )]

    # for perm in permutations(thismove):
    #   xpos = opos
    #   bad = False
    #   for m in perm:
    #     move = movemap[m]
    #     pos2 = addd(move, xpos)
    #     if pos2 not in pad:
    #       bad = True
    #       break
    #     xpos = pos2
    #   if not bad:
    #     poss.append (tuple(perm) + ('A',))
  return []

def go2(pad, c: str, target):
  if not target:
    return [[]]
  asd = []
  c2 = target[0]
  for poss in go(pad, c, c2):
    for rest in go2(pad, c2, target[1:]):
        return [(poss + tuple(rest))]
  return []

# print(list(go2(numpad, 'A', '029A')))

def godirpads(p1, n):
  if n == 0:
    yield p1
    return
  for p2 in go2(dirpad, 'A', p1):
    yield from godirpads(p2, n-1)

def go3(w):
  minl = 100000000000000000000000
  minp = 'a'
  for p1 in go2(numpad, 'A', w):
    for p3 in godirpads(p1, 25):
      if len(p3) < minl:
        minl = len(p3)
        minp = p3
  return minl, int(w.replace('A', '')),minp

def go4(w):
  a,b,c = min(go3(w) for _ in range(100))
  print(a,b,''.join(c))
  return a,b

import sys

sys.setrecursionlimit(15000)

res = 0
for target in lines:
  a,b = go4(target)
  print(a, b,target)
  res += a*b
print(res)





