#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2


from collections import defaultdict, deque
from functools import cache
import heapq
from itertools import pairwise, product

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
  return next(k for k,v in pad.items() if v == c)

@cache
def costofmakingarobotpressthisbutton(thebutton: str, mypos: tuple, deepstate: tuple[tuple,...]):
  if len(deepstate) == 0:
    return [(1,(-1,-1),())]  # at depth 0, all buttons are simply one action to press.
  q = []
  q.append((0,mypos,deepstate,None))
  minw = None
  mindeepstate = []
  seen = {}
  preds = defaultdict(set)
  while q:
    w,pos,deepstate,pred = heapq.heappop(q)
    if w > seen.get(pos, float('inf')):
      continue
    seen[pos] = w
    preds[pos].add(pred)
    if dirpad[pos] == thebutton:
      minw = w
      mindeepstate.append(deepstate)
      continue
    for d in dirs:
      pos2 = addd(d, pos)
      if pos2 not in dirpad: continue
      for cost,botpos,deepstate2 in costofmakingarobotpressthisbutton(charofdir[d], deepstate[0], deepstate[1:]):
        heapq.heappush(q, (w+cost,pos2,(botpos,) + deepstate2,(pos,deepstate)))

  assert minw is not None
  assert mindeepstate

  returns = set()
  thebuttonpos = find(dirpad, thebutton)

  for ds in mindeepstate:
    for w,bp,ds2 in costofmakingarobotpressthisbutton('A', ds[0], ds[1:]):
      w += minw
      finalds = (bp,) + ds2
      returns.add((w,thebuttonpos,finalds))

  # print('returns', len(returns))
  # print('preds', len(preds[thebuttonpos]))

  # after having clicked thebutton, this robot is now on top of thebutton.
  return returns

print(costofmakingarobotpressthisbutton('v', apos, (apos,)))


def getcost(s,n):
  a = 0
  ds = (apos,)*n
  poses = [(0,apos,ds)]
  for c in s:
    newposes = []
    for a,pos,ds in poses:
      asdf = (costofmakingarobotpressthisbutton(c, pos, ds))
      for cost,pos2,ds2 in asdf:
        newposes.append((a+cost,pos2,ds2))
    poses = newposes
  return min(poses)[0]

s = '<A^A>^^AvvvA'
print(len(s))
print(len('v<<A>>^A<A>AvA<^AA>A<vAAA>^A'))
print(len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'))

for n in range(3):
  print(n, getcost(s,n))

print('---')
print(getcost('<<<',1)) # <v<AAA


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

def go(pad, old: str, new: str):
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
    if pos == tgt:
      yield path
      continue
    for d in dirs:
      pos2 = addd(d, pos)
      if pos2 not in pad: continue
      q.append((w+1,pos2,path + [pos2]))

def go2(pad, old, new):
  for path in (go(pad, old, new)):
    # print(path)
    s = ''
    for p1,p2 in pairwise(path):
      s += charofdir[subb(p2,p1)]
    s += 'A'
    yield s

print('paths v')
print(*go2(numpad, 'A', '0'), sep='\n')
print('paths ^')

import sys
d = open('input.txt' if len(sys.argv) == 1 else sys.argv[1]).read()
asd = 0
for l in d.splitlines():
  ol = l
  l = l.split(':')[0]
  # print(l)
  w = 0
  parts = []
  # cartesin product all possible ways to get from between adjacent characters 
  for c1,c2 in pairwise('A' + l):
    parts.append(list(go2(numpad,c1,c2)))
  w += min(getcost(''.join(segments), 25) for segments in product(*parts))
    # w += min(getcost(path, 25) for path in go2(numpad, c1, c2))
  print(l, w, (len(ol.split()[-1])) if ' ' in ol else None)
  asd += w * int(l[:-1], 10)
print(asd)

"""
<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
v<<A>>^A<A>AvA<^AA>A<vAAA>^A
   <   A ^ A >  ^^ A  vvv  A
029A

"""
