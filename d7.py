#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [(x) for x in d.split('\n') if x]

# print(lines)

# print(ints)


from itertools import zip_longest
from functools import lru_cache
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))
def ints(line: str):
  line = ''.join(c if c.isdigit() else ' ' for c in line)
  return [int(x) for x in line.split() if x]

# m = {(r,c):char for r,row in enumerate(lines) for c, char in enumerate(row)}
# print(m)

dirs = [(-1,0), (0,-1), (1,0), (0,1)]
dirs.reverse()
right = lambda asd: dirs[(dirs.index(asd) + 1) % len(dirs)]

rows = []
for l in lines:
  target, rest = l.split(':')
  target = int(target)
  rest = [int(x) for x in rest.split()]
  rows.append((target, rest))

def check(target, x, nums):
  if not nums:
    return x == target
  y, *nums = nums
  return check(target, x+y, nums) or check(target, x*y, nums) or check(target, int(str(x) + str(y)), nums)

y = 0
for target, xs in rows:
  x, *xs = xs
  if check(target, x, xs):
    y += target

print(y)
