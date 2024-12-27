import re, sys, copy, os
from collections import namedtuple

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{e.__class__.__name__}] {e}")
	exit()

# Process the input. There are two parts. The first is a set of initial values for input signals,
# and the second is a list of signals defined as the outputs of logic gates.
parts = input_text.split('\n\n')
init_signals = {line.split(': ')[0]: int(line.split(': ')[1]) for line in parts[0].split('\n')}

def AND(a, b): return a & b
def OR(a, b): return a | b
def XOR(a, b): return a ^ b

Gate = namedtuple('Gate', ['a', 'b', 'op'])
gates = {}
for line in parts[1].split('\n'):
	inputs, output = line.split(' -> ')
	a, opname, b = inputs.split(' ')
	op = AND if opname == 'AND' else OR if opname == 'OR' else XOR
	gates[output] = Gate(a, b, op)

# Part 1: The wires whose names start with 'z' are the bits of a binary number. What is its decimal
# value?
solved = copy.deepcopy(init_signals)
while len(solved) < len(gates) + len(init_signals):
	for output in gates:
		if output in solved:
			continue
		gate = gates[output]
		if gate.a in solved and gate.b in solved:
			solved[output] = gate.op(solved[gate.a], solved[gate.b])

z_outs = sorted([out for out in gates if out[0] == 'z'], reverse = True)
outval = 0
for zo in z_outs:
	outval *= 2
	outval += solved[zo]
print(f"Part 1: The output value is: {outval}")

# Part 2: Four pairs of wires have been swapped, preventing the system from correctly producing the
# sum of the xnn and ynn wires. Find the swapped wires and list their names alphabetically separated
# by commas.








