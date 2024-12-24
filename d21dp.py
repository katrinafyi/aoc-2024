#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2


from collections import defaultdict, deque
from functools import cache
import heapq
from itertools import groupby, pairwise, product

import random


addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)
dirs = [(-1,0), (0,-1), (1,0), (0,1)] # (r,c), turning left, starting from UP
left = lambda asd: dirs[(dirs.index(asd) + 1) % len(dirs)]
right = lambda asd: dirs[(dirs.index(asd) - 1) % len(dirs)]

dirpad = {
  (0,1): '^',
  (0,2): 'A',

  (1,0): '<',
  (1,1): 'v',
  (1,2): '>',
}
apos = next(k for k,v in dirpad.items() if v == 'A')
dirofchar = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}
charofdir = {v:k for k,v in dirofchar.items()}

def find(pad, c):
  if not isinstance(pad, dict): pad = dict(pad)
  try:
    return next(k for k,v in pad.items() if v == c)
  except StopIteration:
    raise ValueError(f"couldn't find {c=} in pad {pad=}") from None

def bfspaths(pad, old: str, new: str):
  src = find(pad, old)
  tgt = find(pad, new)
  q = deque()
  q.append((0, src, [src]))
  seen = {}
  while q:
    w,pos,path = q.popleft()
    if w > seen.get(pos, float('inf')):
      continue
    seen[pos] = w
    if pos == tgt:# and len(list(groupby(path))) <= 2:
      yield path
      continue
    for d in dirs:
      pos2 = addd(d, pos)
      if pos2 not in pad: continue
      q.append((w+1,pos2,path + [pos2]))



"""
A <vA<AA>>^A
A v<<A
A    <
029A
"""

@cache
def costofmakingarobotpressthisbutton(thebutton: str, oldbutton: str, depth: int, *, isnumpad: bool = False) -> tuple[int, str | list]:
  if depth == 0:
    return 1,thebutton

  # XXX: only the deepest level could possibly be a numpad
  pad = numpad if isnumpad else dirpad

  mincost = float('inf')
  minpath = None
  for path in bfspaths(pad, oldbutton, thebutton):
    # print(' ' * (10-depth), oldbutton, 'to', thebutton, path)
    pathcost = 0
    deepbutton = 'A'
    assert all(p in pad for p in path)

    # XXX: moves which we need the robot controlling this robot to perform:
    path = [charofdir[subb(p2,p1)] for p1,p2 in pairwise(path)] + ['A']
    realpath = []
    for movementneeded in path:
      cost2, path2 = costofmakingarobotpressthisbutton(movementneeded, deepbutton, depth-1)
      pathcost += cost2
      realpath.append(path2)
      deepbutton = movementneeded
    assert deepbutton == 'A', 'all deeper robots will be at A'

    if pathcost < mincost:
      mincost = pathcost
      minpath = realpath

  assert isinstance(mincost, int)
  assert minpath
  return mincost, minpath

s = '<A^A>^^AvvvA'
print(len(s))
print(len('v<<A>>^A<A>AvA<^AA>A<vAAA>^A'))
print(len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'))

print('---')
# print(costofmakingarobotpressthisbutton('<', 'A', 2)) # <v<AAA


numpad = {
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
}
def flattenall(xs) -> str:
  return 'disabled'
  if isinstance(xs, str): return xs
  return flattenall(''.join(flattenall(x) for x in xs))

for i in range(5):
  a,b = costofmakingarobotpressthisbutton('<', 'A', i)
  print(i, a, flattenall(b))

import sys
d = open('input.txt' if len(sys.argv) == 1 else sys.argv[1]).read()
asd = 0
for l in d.splitlines():
  ol = l
  l = l.split(':')[0]
  # print(l)
  w = 0
  p = []
  for w2,p2 in (costofmakingarobotpressthisbutton(c2, c1, 26, isnumpad=True) for c1,c2 in pairwise('A' + l)):
    w += w2
    p.append(p2)

  expected = ((ol.split()[-1])) if ' ' in ol else []
  diff = w-len(expected) if expected else None
  print(l, w, len(expected), diff)
  print('have', flattenall(p))
  print('want', expected)
  asd += w * int(l[:-1], 10)
print(asd)

