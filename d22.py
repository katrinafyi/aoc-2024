#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

# /// script
# dependencies = [
# ]
# ///


import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict, Counter, deque
from pprint import pprint

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
def dist(p1, p2):
  x,y = subb(p1,p2)
  return abs(x) + abs(y)

import sys
def ints(line: str):
  line = ''.join(c if c.isdigit() or c == '-' else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

initials = ints(d)
print(initials)

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


def go(secret):
  def prune(x): return secret % 16777216
  def mix(x): return x ^ secret
  secret = mix(secret * 64)
  secret = prune(0)
  secret = mix(secret // 32)
  secret = prune(0)
  secret = mix(secret * 2048)
  secret = prune(0)
  return secret

asd = 0
seens = defaultdict(int)
for n in initials:
  x = n
  seen = {}
  seq = []
  for i in range(2000):
    x2 = go(x)
    seq.append((x2 % 10) - (x % 10))
    if len(seq) > 4:
      seq.pop(0)
    if len(seq) == 4 and tuple(seq) not in seen:
      seen[tuple(seq)] = x2 % 10
    x = x2
  for seq, profit in seen.items():
    seens[seq] += profit
  asd += x
print(asd)
print(max(seens, key=seens.__getitem__))
print(max(seens.values()))

