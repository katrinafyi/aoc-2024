#!/usr/bin/env python3

lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))


lines = [x for x in d.split('\n') if x]
words = [x.split() for x in lines]

# ints = [lmap(int, x) for x in words]

import re

d = open('input.txt').read()
r = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")

x = 0
do = True
for m in re.finditer(r,d):
    if m[0].startswith('mul') and do:
        x += int(m[1]) * int(m[2])
    elif m[0].startswith('don'):
        do = False
    elif m[0].startswith('do'):
        do = True

print(x)

