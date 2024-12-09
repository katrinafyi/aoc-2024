#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

import sys

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [list(x) for x in d.split('\n') if x]

# print(lines)

# print(ints)

# from itertools import combinations, zip_longest
# from functools import lru_cache
# transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))
def ints(line: str):
  line = ''.join(c if c.isdigit() else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [(x) for x in d.split('\n') if x]

addd = lambda x,y: tuple(a+b for a,b in zip(x,y))
subb = lambda x,y: tuple(a-b for a,b in zip(x,y))
mull = lambda x,y: tuple(x*b for b in y)

files = lines[0][::2]
spaces = lines[0][1::2]

print(lines[0])

# print(files)
# print(spaces)

w = sum(int(x) for x in lines[0])
print(w)

disk =[None] * w
j = 0
filelens = {}
for i, filew in enumerate(files):
  filelens[i] = int(filew)
  for x in range(int(filew)):
    disk[j] = i
    j += 1
  if i < len(spaces):
    j += int(spaces[i])

l = 0
r = len(disk)-1
for fileid in reversed(range(len(files))):
  while disk[r] != fileid:
    r -= 1

  # print(''.join([str(c) if c is not None else ' ' for c in disk]))
  match = None
  for l in range(len(disk) - filelens[fileid]):
    if all(l+i < r and disk[l+i] is None for i in range(filelens[fileid])):
      match = l
      break
  if not match: continue


  for i in range(filelens[fileid]):
    disk[r-i] = None
  r -= filelens[fileid]

  for i in range(filelens[fileid]):
    disk[match+i] = fileid

  # print(''.join([str(c) if c is not None else ' ' for c in disk]))



# l = 0
# r = len(disk)-1
# while l < r:
#   while disk[l] is not None:
#     l += 1
#
#   while disk[r] is None:
#     r -= 1
#
#   disk[l] = disk[r]
#   disk[r] = None
#
# while disk[-1] is None:
#   disk.pop()
#
# disk[-2] = disk[-1]
# disk[-1] = None
# disk.pop()
#

res = 0
for i, c in enumerate(disk):
  if c is not None:
    res += i*c
print(res)



#
