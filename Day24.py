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
num_bits = len(init_signals) // 2

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
# value? I'm rewriting this as a function that checks for hanging to help with part 2.
def solve_gates(input_gates, init_signals):
	in_gates = copy.deepcopy(input_gates)
	solved = copy.deepcopy(init_signals)
	while len(solved) < len(in_gates) + len(init_signals):
		solved_one_gate = False
		for output in in_gates:
			if output in solved:
				continue
			gate = in_gates[output]
			if gate.a in solved and gate.b in solved:
				solved_one_gate = True
				solved[output] = gate.op(solved[gate.a], solved[gate.b])
		if not solved_one_gate:
			break
	return solved

solved = solve_gates(gates, init_signals)
z_outs = sorted([out for out in gates if out[0] == 'z'], reverse = True)
outval = 0
for zo in z_outs:
	outval *= 2
	outval += solved[zo]
print(f"Part 1: The output value is: {outval}")

# Part 2: Four pairs of gates have had their output wires swapped, preventing the system from
# correctly producing the sum of the xnn and ynn wires. Find the swapped wires and list their
# names alphabetically separated by commas. After trying and failing to use test vectors to
# identify bad gates, I think the easiest thing to do is to identify the gates for each bit.
# The first bits are added with a half adder:
#
#  z00 = x00 xor y00
#  co00 = x00 and y00
#
# Subsequent bits are added with full adders. Note that the final sum's carry out is used to
# produce an extra output bit!
#
#  sn = xn xor yn
#  csn = xn and yn
#  zn = sn xor cin
#  cscn = sn and cin
#  con = csn or cscn
#
# With this, we can identify each gate and try to check the connections.
def find_gate(input1, input2, gate_type, input_gates):
	for gate in input_gates:
		a = input_gates[gate].a
		b = input_gates[gate].b
		op = input_gates[gate].op
		if (a == input1 or b == input1 or not input1) and (a == input2 or b == input2 or not input2) and op == gate_type:
			return gate
	#print(f"Couldn't find gate: {input1} {gate_type.__name__} {input2}")
	return None

def check_gates_for_bit(bit, input_gates):
	ns = f'{n:02}'
	s = find_gate('x' + ns, 'y' + ns, XOR, input_gates)
	cs = find_gate('x' + ns, 'y' + ns, AND, input_gates)
	z = 'z' + ns
	if input_gates[z].op != XOR:
		print(f"Bit {bit} Z gate has wrong type! {input_gates[z].a} {input_gates[z].op.__name__} {input_gates[z].b}")
	if input_gates[z].a != s and input_gates[z].b != s:
		print(f"Bit {bit} S gate misdirected! Z inputs were {input_gates[z].a} and {input_gates[z].b}")
	ci = input_gates[z].a if input_gates[z].a != s else input_gates[z].b
	csc = find_gate(s, ci, AND, input_gates)
	if not csc:
		print(f"Bit {bit} CSC gate has bad inputs! {s} and {ci}")
	co = find_gate(cs, csc, OR, input_gates)
	if not co:
		print(f"Bit {bit} CO gate has bad inputs! {cs} and {csc}")

def swap_signals(input_gates, sig1, sig2):
	new_gates = copy.deepcopy(input_gates)
	temp = new_gates[sig1]
	new_gates[sig1] = new_gates[sig2]
	new_gates[sig2] = temp
	return new_gates

# I found these manually, print()ing out connections for suspicious-looking gates and swapping
# them until the bit passed the gate check. It turned out that all of the swaps were localized
# to individual full adder circuits.
ng = swap_signals(gates, 'z16', 'hmk')
ng = swap_signals(ng, 'z20', 'fhp')
ng = swap_signals(ng, 'rvf', 'tpc')
ng = swap_signals(ng, 'z33', 'fcd')
for n in range(1, num_bits):
	check_gates_for_bit(n, ng)
	
swap_list = ['z16', 'hmk', 'z20', 'fhp', 'rvf', 'tpc', 'z33', 'fcd']
result = ','.join(sorted(swap_list))
print(f"Part 2: The list of swapped gates is: {result}")
