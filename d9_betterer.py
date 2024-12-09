#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))

import heapq

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [list(x) for x in d.split('\n') if x]

# print(lines)

# print(ints)

from itertools import combinations, zip_longest
from functools import lru_cache
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))
def ints(line: str):
  line = ''.join(c if c.isdigit() else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [(x) for x in d.split('\n') if x]

addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)

files = lmap(int, lines[0][::2])
spaces = lmap(int, lines[0][1::2])

# print(lines[0])

# print(files)
# print(spaces)

w = sum(files) + sum(spaces)
print(w)

# flat memory array
disk: list[None | int] = [None] * w

# list of lists of gaps.
# gaps[w] is a sorted list of positions of gap size w
gaps: list[list[int]] = [None] + [[] for _ in range(9)] # type: ignore

l = 0
fileposes = []
for i, w in enumerate(files):
  fileposes.append((l, i, w))
  for j in range(w):
    disk[l + j] = i
  l += w
  if i < len(spaces) and spaces[i]:
    gaps[spaces[i]].append(l)
    l += spaces[i]

l = 0
r = len(disk)-1
while l < r:
  while disk[l] is not None:
    l += 1
  while l < r and disk[r] is None:
    r -= 1

  disk[l] = disk[r]
  disk[r] = None

while disk[-1] is None:
  disk.pop()

res = 0
for i, c in enumerate(disk):
  if c is not None:
    res += i*c
print(res)

finalpos = []
for pos,fileid,w in reversed(fileposes):
  gappos, gapw = min(((g[0], gw) for gw, g in enumerate(gaps) if g and gw >= w), default=(w, 0))
  if gappos >= pos:
    finalpos.append((pos, fileid, w))
    continue

  heapq.heappop(gaps[gapw])
  if gapw-w > 0:
    heapq.heappush(gaps[gapw-w], gappos+w)

  finalpos.append((gappos, fileid, w))

asd = 0
for pos,id,w in finalpos:
  asd += sum(id*(pos+i) for i in range(w))
print(asd)
