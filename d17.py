#!/usr/bin/env python3
# vim: ts=2 sts=2 et sw=2

# /// script
# dependencies = [
#   "scipy",
# ]
# ///
import sys
def ints(line: str):
  line = ''.join(c if c.isdigit() or c == '-' else ' ' for c in line)
  return [int(x) for x in line.split() if x]

d = open(sys.argv[1] if len(sys.argv) >= 2 else 'input.txt').read()

r, p = d.split('\n\n')
regs = ints(r)
prog = ints(p)
#
# lines = [list(x.strip()) for x in d.split('\n') if x]
#
# m = {(r,c):(char) for r,row in enumerate(lines) for c, char in enumerate(row)}
#
# movemap = {
#   '^': (-1, 0),
#   '<': (0,-1),
#   '>': (0,1),
#   'v': (1,0)
# }

print(regs)
print(prog)

regs0 = regs.copy()
def go(a: int):
  regs = regs0.copy()
  regs[0] = a

  def combo(x):
    def set(val):
      regs[x-4] = val
    if 0 <= x <= 3:
      return x, None
    if 4 <= x <= 6:
      return regs[x-4], None
    assert False, 'wrong operand'

  output = []
  ip = 0
  wrong = False
  while ip < len(prog):
    # if len(output) > len(prog): 
    #   wrong = True
    #   break
    jumped = False

    opcode = prog[ip]
    opn = prog[ip+1]
    # print(ip, opcode, opn)

    if opcode == 0:
      num = regs[0]
      den = 2**combo(opn)[0]
      regs[0] = num // den
    elif opcode == 1:
      regs[1] = regs[1] ^ opn
    elif opcode == 2:
      regs[1] = combo(opn)[0] % 8
    elif opcode == 3:
      if not regs[0]:
        pass
      else:
        ip = opn
        jumped = True
    elif opcode == 4:
      regs[1] = regs[1] ^ regs[2]
    elif opcode == 5:
      output.append(combo(opn)[0] % 8)
      # print(combo(opn)[0] % 8, end=',', flush=True)
    elif opcode == 6:
      num = regs[0] // 2**combo(opn)[0]
      regs[1] = num
    elif opcode == 7:
      num = regs[0] // 2**combo(opn)[0]
      regs[2] = num

    if not jumped:
      ip += 2

  # print(a)
  return output


# i = 0
# prev = 0
# while prev < 10:
#   l = len(go(i))
#   if l > prev:
#     print(i)
#     prev = l
#   i += 1
#
# raise 0
#
cumsum = 0
for i in range(len(prog)):
  cumsum += 8 ** i

cumsum = 8 ** (len(prog))
print()
print(go(cumsum-1))
print(go(cumsum))
print(go(cumsum+1))
print()

cumsum -= 1

magnitude = len(prog) - 1
j = len(prog) - 1

coeffs = []
for target in reversed(prog):
  print()
  print(prog)
  print([0 if i != j else 1 for i in range(len(prog))])
  # if magnitude > 0:
  #   asd = 0
  #   while go(cumsum)[j+1:] == go(cumsum + asd * 8 ** (magnitude-1))[j+1:]:
  #     asd += 1
  #   asd -= 1
  #   print('asd', asd)

  # if magnitude == 6:
  #   cumsum -= 8 ** (magnitude-1)
  for i in (range(8)):
    offset = i * 8 ** magnitude
    result = (go(cumsum - offset))
    if magnitude > 0:
      assert result[j] == go(cumsum - offset - 7*8**(magnitude-1))[j], "still at the top of the lesser magnitude"
    print('match coeff', i, 'at index', j)
    print(result)
    if result[j] == target:
      coeffs.append(i)
      print('... matched!')
      cumsum -= offset
      # cumsum += (i) * 8 ** (magnitude - 1)
      break
  else:
    coeffs.append(None)
    print('no match at index', j, ':(((((', 'magnitude', magnitude)
    # break
  magnitude -= 1
  j -= 1
print(cumsum)

original = cumsum

print(prog, 'asd')
print()
for i in range(10):
  print(go(cumsum - i * 8**6))

print(coeffs)
print('have', go(cumsum))
print('want', prog)

num = 0
for c in coeffs:
  num *= 8
  num += (8-c) if c is not None else 0
print(num)

assert go(cumsum) == prog

a = 38886633881076
while go(a) != prog:
  a += 1

print(a)


# assert go(cumsum) == prog
