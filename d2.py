lmap = lambda f, xs: list(map(f, xs))
from collections import defaultdict

def rreplace(x, old, new):
    return new.join(x.rsplit(old, 1))

d = open('input.txt').read()

lines = [x for x in d.split('\n') if x]
words = [x.split() for x in lines]

ints = [lmap(int, x) for x in words]
def safe(x):

    for i in range(len(x)+1):
        y = False
        z = x[:i] + x[i+1:]

        y |= z == list(sorted(z)) or z == list(sorted(z, reverse=True))
        y &= all(1 <= abs(a-b) <= 3 for a,b in zip(z, z[1:]))

        if y: return y

safed = [x for x in ints if safe(x)]
print(len(safed))


print(len(safed))

left = [x[0] for x in ints]
right = [x[1] for x in ints]

left.sort()
right.sort()


counts = defaultdict(int)
for x in right:
    counts[x] += 1

x = 0
for l in left:
    x += l * counts[l]
print(x)
