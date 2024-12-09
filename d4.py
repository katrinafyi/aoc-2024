#!/usr/bin/env python3

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


d = open('input.txt').read()
lines = [list(x) for x in d.split('\n') if x]
# words = [x.split() for x in lines]

# ints = [lmap(int, x) for x in words]

from itertools import zip_longest
transpose = lambda x: list(map(list, zip_longest(*x, fillvalue=' ')))

x = 0
x += '\n'.join(''.join(x) for x in lines).count('XMAS')
x += '\n'.join(''.join(x) for x in lines).count('XMAS'[::-1])
x += '\n'.join(''.join(x) for x in transpose(lines)).count('XMAS')
x += '\n'.join(''.join(x) for x in transpose(lines)).count('XMAS'[::-1])

diags = [list(' ' * i) + x for i, x in enumerate(lines)]
x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS')
x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS'[::-1])
# x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS')
# x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS'[::-1])


diags = [list(' ' * (len(lines)-1-i)) + x for i, x in enumerate((lines))]
x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS')
x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS'[::-1])
# x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS')
# x += '\n'.join(''.join(x) for x in transpose(diags)).count('XMAS'[::-1])

m = {(r,c):char for r,row in enumerate(lines) for c, char in enumerate(row)}

print(x)

y = 0

for (r,c),char in m.items():
    if char != 'A': continue 
    a, b = m.get((r+1,c+1)), m.get((r-1,c-1))
    if {a,b} != {'M', 'S'}: continue
    a, b = m.get((r-1,c+1)), m.get((r+1,c-1))
    if {a,b} != {'M', 'S'}: continue
    y += 1

print(y)


