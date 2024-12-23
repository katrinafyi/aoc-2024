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
  apos = find('A')
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

      mov = '>' if dc > 0 else '<'
      if dc != 0 and addd(movemap[mov], pos) in pad and cpos[0] != apos[0]:
        thismove.append(mov)
        pos = addd(movemap[mov], pos)
        continue

      mov = 'v' if dr > 0 else '^'
      if dr != 0 and addd(movemap[mov], pos) in pad:
        thismove.append(mov)
        pos = addd(movemap[mov], pos)
        continue


      mov = 'v' if dr > 0 else '^'
      if dr != 0 and addd(movemap[mov], pos) in pad:
        thismove.append(mov)
        pos = addd(movemap[mov], pos)
        continue
      mov = '>' if dc > 0 else '<'
      if dc != 0 and addd(movemap[mov], pos) in pad:
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
        asd.append (poss + tuple(rest))
  return asd

# print(list(go2(numpad, 'A', '029A')))

def go3(w):
  minl = 100000000000000000000000
  minp = 'a'
  for p1 in go2(numpad, 'A', w):
    for p2 in go2(dirpad, 'A', p1):
      for p3 in go2(dirpad, 'A', p2):
        if len(p3) < minl:
          minl = len(p3)
          minp = p1,p2,p3
          # if w == '379A':
          #   print(''.join(p3))
  return minl, int(w.replace('A', '')),minp

def go4(w):
  a,b,c = min(go3(w) for _ in range(1))
  print(a,b)
  for asd in c:
    print(''.join(asd))
  return a,b

# res = 0
# for target in lines:
#   a,b = go4(target)
#   print(a, b,target)
#   res += a*b
# print(res)
#
'''
so we want to do an inductive shortest path algorithm
where edge weights are the length of the _final_ string which
is needed to make that movement
how do we induct???

num[0,2] = min_(p in paths) (sum(dpad[p1,p2] for p1,p2 in sliding(p)))

where paths includes clicking A 

basest[x,y] = 1

'''

def shortestpath(pad, start, weights):
  # weights maps the directional movement to the cost of that movement.
  def find(c):
    return next(k for k,v in pad.items() if v == c)

  start = find(start)

  seen = {}
  q = []
  q.append((0,start,None))

  while q:
    w, pos,pred = heapq.heappop(q)
    if pos in seen:
      if w == seen[pos][0]:
        seen[pos][1].add(pred)
      continue
    seen[pos] = (w,{pred})
    for d in dirs:
      pos2 = addd(d, pos)
      cost = weights[d]
      assert cost >= 1
      if pos2 in pad and pos2 not in seen:
        heapq.heappush(q, (w+cost,pos2,d))

  return seen

def getpaths(preds, start, end):
  q = deque()
  q.append([end,()])
  seen = set()
  endpaths = []
  while q:
    print(q)
    pos,path = q.popleft()
    if pos == start:
      endpaths.append(path)
    for d in preds[pos][1]:
      if d is None: continue
      pos2 = subb(pos, d)
      q.append((pos2, (pos2,) + path))
  return endpaths

from pprint import pprint

asdf = (shortestpath(dict(numpad), 'A', defaultdict(lambda: 1)))
pprint(asdf)
pprint(getpaths(asdf, (3,2), (0,0)))

dircosts = defaultdict(lambda: 1)
for i in range(2):
  result = (shortestpath(dict(dirpad), 'A', dircosts))

"""
dist[<,^] = min_(p in paths) (sum(prevdist[p1,p2] for p1,p2 in sliding(p)))
"""
