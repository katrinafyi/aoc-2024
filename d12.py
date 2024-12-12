#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

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
lines = [list(x) for x in d.split('\n') if x]

m = {(r,c):(char) if char != '.' else None for r,row in enumerate(lines) for c, char in enumerate(row)}

uniq = set((m).values())

print(uniq)

x = 0
regions = {}

for u in uniq:
  poses = {k for k,v in m.items() if v == u}

  seen = set()

  while poses:
    pos = next(iter(poses))
    chunk = set()
    q = [pos]
    while q:
      pos = q.pop()
      if pos in seen: continue
      chunk.add(pos)
      seen.add(pos)
      for d in dirs:
        pos2 = addd(pos,d)
        if m.get(pos2) == u and pos2 not in seen:
          q.append(pos2)
    # print(chunk)
    poses -= chunk


    area = len(chunk)
    sides = 1

    adjacencies = []
    for p in chunk:
      for d in dirs:
        p2 = addd(p,d)
        if p2 not in chunk:
          adjacencies.append((p,p2))
    verts = [(p,p2) for p,p2 in adjacencies if p[0] == p2[0]]
    verts = [(x[::-1], y[::-1]) for x,y in verts]
    verts.sort()
    horiz = [(p,p2) for p,p2 in adjacencies if p[1] == p2[1]]
    horiz.sort()
    assert len(horiz) + len(verts) == len(adjacencies)

    # horizontals: sides which are horizontal (i.e. adjacencies have the same column)
    # sorted by column

    sides = 0
    for theside in [horiz, verts]:
      seen = set()
      for p,p2 in theside:
        left = (0,-1)
        assert addd(p,left) != p2
        assert subb(p,left) != p2
        assert addd(p2,left) != p
        assert subb(p2,left) != p
        if (p,p2) not in seen and (addd(p,left),addd(p2,left)) not in seen:
          sides += 1
        seen.add((p,p2))

    #
    # edge = next(iter(p for p in chunk if any((addd(p,d)) not in chunk for d in dirs)))
    # try:
    #   dir = next(iter(d for d in dirs if addd(edge,d) in chunk))
    #   # print(edge,dir)
    #   seen2 = set()
    #   pos = edge
    #   while True:
    #     if (pos,dir) in seen2: break
    #     seen2.add((pos,dir))
    #     if addd(pos,dir) in chunk:
    #       pos2 = addd(pos,dir)
    #       if addd(pos2, right(dir)) not in chunk:
    #         pos = pos2
    #         continue
    #       pos = addd(pos2, right(dir))
    #       dir = right(dir)
    #       continue
    #     dir = left(dir)
    #     sides += 1
    # except StopIteration:
    #   sides = 4


    x += area * sides
    print(u, area, sides)

print(x)



