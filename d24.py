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
def dist(p1, p2): return sum(map(abs, subb(p1,p2)))

import sys
import heapq
def ints(line: str):
  line = ''.join(c if c.isdigit() or c == '-' else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

#
#
# m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}
#
movemap = {
  '^': (-1, 0),
  '<': (0,-1),
  '>': (0,1),
  'v': (1,0)
}

# clear = {k for k,v in m.items() if v in '.SE'}
# start = next(k for k,v in m.items() if v == 'S')
# end = next(k for k,v in m.items() if v == 'E')
#
# print(clear, start, end)


up, down = d.split('\n\n')

initial = [x.replace(':', '').split() for x in up.splitlines() if x]
gates = [x.replace('-> ', '').split(' ') for x in down.split('\n') if x]
# print(gates)
# print(initial)

def go(initial, gates, realgates):
  allows = defaultdict(set)
  for a,op,b,out in gates:
    allows[a].add((a,op,b,out))
    allows[b].add((a,op,b,out))

  def getdigit(prefix):
    zs = list(sorted((k,v) for k,v in vals.items() if k.startswith(prefix)))
    zs.reverse()
    return (int(''.join('1' if x else '0' for _,x in zs), 2))

  vals = {}
  for k,v in initial:
    vals[k] = v == '1'
  x,y = (getdigit('x'), getdigit('y'))
  # print(lmap(hex,[x,y,x+y]))

  faketoreal = {}
  realtofake = {}
  for k in vals:
    # realk = swaps.get(k,k)
    realk = k
    faketoreal[k] = realk
    realtofake[realk] = k

  q = set()
  for k in vals:
    q |= (allows[k])

  while q:
    # print(q)
    # print(faketoreal)
    new = set()
    for a,op,b,out in list(q):
      assert a in vals or b in vals
      if out in vals: continue
      if a in vals and b in vals:
        if op == 'AND':
          f = lambda a,b: a and b
        elif op == 'OR':
          f = lambda a,b: a or b
        elif op == 'XOR':
          f = lambda a,b: a != b
        else:
          assert False
        a2 = faketoreal[a]
        b2 = faketoreal[b]
        op2 = op
        # print(a2,op2,b2, '-> fake', out, end='')
        try:
          ra,rop,rb,rout = next((a,op,b,out) for a,op,b,out in realgates if {a,b} == {a2,b2} and op == op2)
        except StopIteration:
          print('\nfailed to match. one of these assignments is wrong:', a2, b2)
          # XXX: tacitly assumes that at most one input of a gate is swapped.
          possiblera = [(a if b2 != a else b,a2) for a,op,b,out in realgates if b2 in {a,b} and op == op2]
          possiblerb = [(a if a2 != a else b,b2) for a,op,b,out in realgates if a2 in {a,b} and op == op2]
          possibleswaps = set(map(frozenset,possiblera + possiblerb))
          # frozenset + inline if/else deals with commutativity
          print('possible recovering swaps', possibleswaps)
          return False, -1, realtofake, possibleswaps
        # print(' = real', rout, '?')
        if out in faketoreal:
          print('attempting to reassign fake', out, 'to real', rout, 'but was already real', faketoreal[out])
          assert False, 'surely not. invalid visit order??'
        # if rout in swaps:
        #   print('SWAPPING!!!', out, 'via', {rout, swaps[rout]})
        #   rout = swaps[rout]
          # _,_,_,otherout = next((a,op,b,out) for a,op,b,out in realgates if {a,b} == {a,b} and op == op2)
        faketoreal[out] = rout
        realtofake[rout] = out

        vals[out] = f(vals[a] , vals[b])
        new |= allows[out]

    q = new
  # print(faketoreal)
  assert set(allows) == set(vals)

  return True, getdigit('z'), realtofake, set()

print('part1', go(initial, gates, gates)[:2])


realgates = []
maxvar = max(initial)[0]
print('found largest variable', maxvar)
count = int(maxvar[1:]) + 1
for i in range(count):
  ii = f'{i:02}'
  y = f'y{ii}'
  x = f'x{ii}'
  cprev = f'carry{(i-1):02}'
  carry = f'carry{(i):02}'

  # https://www.build-electronic-circuits.com/full-adder/
  if i == 0:
    realgates.append((x, 'XOR', y, f'z{ii}'))
    realgates.append((x, 'AND', y, carry))

  elif i > 0:
    realgates.append((x, 'XOR', y, f'partialsum{ii}'))
    realgates.append((x, 'AND', y, 'partial' + carry))

    realgates.append((f'partialsum{ii}', 'XOR', cprev, f'z{ii}'))
    realgates.append((cprev, 'AND', f'partialsum{ii}', f'partialsumandcprev{ii}'))
    if i == count-1:
      realgates.append(('partial' + carry, 'OR', f'partialsumandcprev{ii}', f'z{(i+1):02}'))
    else:
      realgates.append(('partial' + carry, 'OR', f'partialsumandcprev{ii}', f'carry{ii}'))

# XXX: for the competition submission, we manually identified
# swaps when running `go` and seeing a StopIteration.

# swaps['z11'] = 'partialcarry11'
# swaps['z24'] = 'carry24'
# swaps['partialcarry28'] = 'partialsum28'
# swaps['z38'] = 'partialsumandcprev38'

realgates0 = realgates.copy()

swaps = None
realtofake = None
ok = False
swapq = [{}]
while not ok and swapq:
  swaps = swapq.pop()
  realgates = [(a,op,b,swaps.get(out,out)) for a,op,b,out in realgates0]
  ok, _, realtofake, swapoptions = go(initial, gates, realgates)
  for a,b in swapoptions:
    swapq.append(swaps.copy() | {a:b, b:a})

assert ok, 'something has gone wrong and we did not succeed the swapping'
assert realtofake and swaps

print()
print('swaps:', *set(map(frozenset, swaps.items())), sep='\n')
print(','.join(list(sorted(realtofake[r] for r in swaps))))







