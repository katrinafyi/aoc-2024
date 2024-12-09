#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

# /// script
# dependencies = [
#   "sortedcontainers",
# ]
# ///

import sys

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()
lines = [(x) for x in d.split('\n') if x]

def chunks(lst, n):
    for i in range(0, len(lst), n): yield lst[i:i + n]

from sortedcontainers import SortedDict, SortedList

# map of starting pos to (width, fileid or None) pairs. None indicates space
disk: SortedDict = SortedDict()

# map of pos to gap width
spaces: SortedDict = SortedDict()

l = 0
line = [int(x) for x in lines[0]] + [0]
for i, (filew, spacew) in enumerate(chunks(line, 2)):
  disk[l] = (filew, str(i))
  l += filew
  if spacew:
    spaces[l] = spacew
  l += spacew

def move(start: int, w: int, dest: int):
  startbase = next(disk.irange(maximum=start, reverse=True))
  old = disk[startbase]
  assert w <= old[0], "move width too big"
  assert start + w == startbase + old[0], "can only move from the right!"
  if old[0] == w:
    del disk[startbase]
  else:
    disk[startbase] = (old[0] - w, old[1])
  spaces[start] = w # XXX: spaces not merged on right

  destleft = next(disk.irange(maximum=dest, reverse=True))
  destright = next(disk.irange(minimum=dest, reverse=False))
  destleftend = destleft + disk[destleft][0]
  assert dest == destleftend, "can only move into the left side of a gap!"
  assert spaces[destleftend] >= w, "too small 2"
  disk[dest] = (w, old[1])
  spacew = destright - destleftend
  del spaces[destleftend]
  spacew -= w
  assert spacew >= 0, "moving into a gap which is too small!"
  if spacew:
    spaces[dest + w] = spacew

def space_for(spacew: int, before: int) -> int | None:
  for pos, w in spaces.items():
    if pos + spacew > before: break
    if w >= spacew:
      return pos
  return None

# disk0 = disk.copy()
# spaces0 = spaces.copy()
#
# while True:
#   lastbase, (w, c) = disk.peekitem()
#   space = space_for(1, lastbase)
#   if not space: break
#   move(lastbase + w - 1, 1, space)
#
# res = 0
# for pos, (w,c) in disk.items():
#   res += sum(int(c)*(pos+i) for i in range(w))
# print(res)
#
# disk = disk0
# spaces = spaces0

for pos, (w,c) in list(reversed(disk.items())):
  space = space_for(w, pos)
  if space is None: continue
  move(pos, w, space)

res = 0
for pos, (w,c) in disk.items():
  res += sum(int(c)*(pos+i) for i in range(w))
print(res)
