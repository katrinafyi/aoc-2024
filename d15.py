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

grid, moves = d.split('\n\n')
d = grid.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')
lines = [list(x.strip()) for x in d.split('\n') if x]

m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}

walls = set()
boxes = dict()
robot = next(iter(k for k,v in m.items() if v == '@'))
for pos, ch in m.items():
  if ch == '#': walls.add(pos)
  if ch in '[]':
    other = (0,-1) if ch == ']' else (0,1)
    pos2 = addd(other, pos)
    boxes[pos] = [pos, pos2]
    boxes[pos2] = boxes[pos]

print(walls, boxes, robot)

# from scipy.optimize import linprog
import math

from fractions import Fraction
import heapq


moves = moves.replace('\n', '')

print(m, moves)

pos = next(iter(k for k,v in m.items() if v == '@'))
m[pos] = '.'

print(pos)

movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

def printgrid():
  for r in range(-16, 16):
    r += pos[0]
    for c in range(-16, 16):
      c += pos[1]
      if (r,c) in walls:
        ch = '#'
      elif (r,c) in boxes:
        ch = '!'
      else:
        ch = ' '
      if (r,c) == pos:
        assert ch == ' '
        ch = '@'
      print(ch, end='')
    print()

from collections import deque

print(pos, m)
for mov in moves.strip():
  dir = movemap[mov]
  pos2 = addd(pos, dir)

  if pos2 not in walls and pos2 not in boxes:
    pos = pos2
    print('no boxes, moving to', pos2)
    printgrid()
    continue
  if pos2 in walls: continue


  # in boxes
  blocked = False
  seen = set()
  order = []
  q = deque()
  q.append(boxes[pos2])
  while q:
    # print(q)
    pair = q.popleft()
    assert len(pair) == 2
    assert len(pair[0]) == 2
    if tuple(pair) in seen: continue
    order.append(tuple(pair))
    seen.add(tuple(pair))
    if any(addd(dir, p) in walls for p in pair):
      blocked = True
      break
    for p in pair:
      if addd(dir, p) in boxes:
        q.append(boxes[addd(dir, p)])

  if blocked:
    print('blocked')
    continue

  assert len(set(order)) == len(order)

  print(mov, 'moving', len(order), 'boxes', order)
  for a,b in reversed(order):
    del boxes[a]
    del boxes[b]
    new = [addd(dir, a), addd(dir, b)]
    boxes[new[0]] = new
    boxes[new[1]] = new
  pos  = pos2
  printgrid()

  assert (all(k in v and len(v) == 2 for k,v in boxes.items()))
  for k,v in boxes.items():
    assert k in v
    for other in v:
      assert boxes.get(other) is v, f'box {k=} is missing its companion at {other=}'
  count = defaultdict(list)
  for pair in set(lmap(tuple,boxes.values())):
    count[pair[0]].append(pair)
    count[pair[1]].append(pair)
  for k,v in count.items():
    assert len(v) == 1, f'{k=} has {v=}'


ans = 0
for a,b in set(tuple(x) for x in boxes.values()):
  r,c = min(a,b)
  ans += 100*r + c
print(ans)
