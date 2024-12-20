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
lines = [list(x.strip()) for x in d.split('\n') if x]
#
m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}
#
movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

poses = list(tuple(ints(x)) for x in d.split('\n') if x)
# print(poses)


clear = {k for k,v in m.items() if v in '.SE'}

# print(clear)

start = next(k for k,v in m.items() if v == 'S')
end = next(k for k,v in m.items() if v == 'E')

# print(clear, start, end)

import heapq

saved = defaultdict(int)
#
# def go(hackpos, hackdir):
#   seen = set()
#   q = []
#   nohacks = ((-1,-1), (0,0))
#   q.append((0,nohacks, start,0,0))
#   while q:
#     print(len(q))
#     w, hacked, pos, hacks,l = heapq.heappop(q)
#     if (hacked, pos, hacks) in seen: continue
#     if pos == end and hacked == nohacks:
#       return w
#     if hacks <= 0 and pos not in clear:
#       continue  # segfault
#     seen.add((hacked, pos, hacks))
#     hacks2 = max(hacks-1, 0)
#     for d in dirs:
#       pos2 = addd(d, pos)
#       poss = pos2 in clear or hacks > 0
#       if poss and (hacked, pos2, hacks2) not in seen:
#         heapq.heappush(q, (w+1, hacked, pos2, hacks2, l+1))
#       if not hacked and ((pos2,d),pos2,1) not in seen:
#         heapq.heappush(q, (w, (pos2, d), pos2, 1, l))


def guess(pos):
  return abs(pos[0]-end[0]) + abs(pos[1]-end[1])

def go():
  seen = set()
  q = []
  q.append((0,0,False,start,None,None))

  finishedat = {}

  finished = set()

  while q:
    # print(len(q))
    _,w, hacked, pos, hackpos,hackd = heapq.heappop(q)
    # if w > 9505: break
    if (hacked,pos,hackpos,hackd) in seen: continue
    if (hackpos,hackd) in finished: continue
    if pos == end and (hackpos,hackd) not in finishedat:
      finished.add((hackpos,hackd))
      finishedat[hackpos,hackd] = w
      continue
    # if hacks <= 0 and pos not in clear:
    #   continue  # segfault
    seen.add((hacked,pos,hackpos,hackd))
    for d in dirs:
      pos2 = addd(d, pos)
      if pos2 in clear and (hacked, pos2,hackpos,hackd) not in seen:
        heapq.heappush(q, (w+1+guess(pos2),w+1, hacked, pos2, hackpos, hackd))
      if addd(pos2, d) in clear:
        if not hacked and (True, addd(pos2,d),pos2,d) not in seen:
          heapq.heappush(q, (w+2+guess(addd(pos2,d)),w+2, True, addd(pos2,d), pos2, d))


  return finishedat

def go2(start,end):
  seen = {}
  q = []
  q.append((0,start))

  while q:
    # print(len(q))
    w, pos = heapq.heappop(q)
    if pos in seen: continue
    seen[pos] = w
    # if hacks <= 0 and pos not in clear:
    #   continue  # segfault
    for d in dirs:
      pos2 = addd(d, pos)
      if pos2 in clear and pos2 not in seen:
        heapq.heappush(q, (w+1,pos2))

  return seen

forw = go2(start, end)
back = go2(end, start)

base = forw[end]

cuts = defaultdict(set)

def dist(p1, p2):
  x,y = subb(p1,p2)
  return abs(x) + abs(y)

@cache
def step(n, pos):
  if n == 0:
    return {pos}
  res = {pos}
  for d in dirs:
    p2 = addd(d, pos)
    res |= (step(n-1, p2))
  return res

print(list(step(1, (0,0))))
# print(len(list(step(21, (0,0)))))
# raise 0

assert forw[start] == 0
assert back[end] == 0

# for p in clear:
#   print('asd', p)
#   print( set(p2 for p2 in clear if dist(p,p2) <= 2) - (set(step(3, p)) & clear))
#   break

for p in clear:
  # for p2 in step(20, p):
  for p2 in clear:
    if p == p2: continue
    if dist(p,p2) <= 20 and p2 != p:
      if p2 in clear and p in clear:
        cost = back[p] + dist(p,p2) + forw[p2]
        cuts[base - cost].add((p,p2))
# print(cuts)

res = 0

from pprint import pprint
aa = [(len(cs), saved)for saved,cs in cuts.items() if saved >= 50]
aa.sort(key=lambda x: x[1])
pprint(aa)

for s,asd in cuts.items():
  if s >= 100: res += len(asd)
print(res)

# saved = go()
# print(saved)









