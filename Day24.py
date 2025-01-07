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
# names alphabetically separated by commas. Since this is a binary adder, I can try each bit
# one at a time to narrow down which gates are involved.
def run_gates(input_gates, x, y):
	xb = {f'x{n:02}': (x // 2**n) & 1 for n in range(num_bits)}
	yb = {f'y{n:02}': (y // 2**n) & 1 for n in range(num_bits)}
	solved = solve_gates(input_gates, xb | yb)
	z = sum(solved[f'z{n:02}'] * 2**n for n in range(num_bits))
	return z % 2**num_bits

def check_bit(input_gates, bit):
	try:
		mask = 2**bit
		ci_mask = mask >> 1
		all_ones = 2**num_bits - 1
		inv_mask = all_ones ^ mask
		inv_ci_mask = all_ones ^ ci_mask
		zx = run_gates(input_gates, mask, 0)
		zy = run_gates(input_gates, 0, mask)
		zci = run_gates(input_gates, ci_mask, ci_mask)
		zco = run_gates(input_gates, mask, mask)
		inv_zx_bit = run_gates(input_gates, inv_mask, 0) & mask
		inv_zy_bit = run_gates(input_gates, 0, inv_mask) & mask
		inv_zc_bit = run_gates(input_gates, inv_ci_mask, inv_ci_mask) & mask
	except Exception as e:
		return False
	if zx != mask or zy != mask or zci != ci_mask + ci_mask or zco != (mask + mask) % 2**num_bits:
		return False
	if inv_zx_bit != 0 or inv_zy_bit != 0 or inv_zc_bit != 0:
		return False
	return True

def swap_signals(input_gates, sig1, sig2):
	new_gates = copy.deepcopy(input_gates)
	temp = new_gates[sig1]
	new_gates[sig1] = new_gates[sig2]
	new_gates[sig2] = temp
	return new_gates

gate_names = list(gates.keys())
for n in range(35, num_bits):
	print(f"Bit {n}")
	bit_good = check_bit(gates, n)
	if not bit_good:
		for g1 in range(len(gate_names) - 1):
			for g2 in range(g1+1, len(gate_names)):
				new_gates = swap_signals(gates, gate_names[g1], gate_names[g2])
				bit_good = check_bit(new_gates, n)
				if bit_good:
					print(f"Would swap {gate_names[g1]} and {gate_names[g2]}")
					break
			if bit_good:
				break


# qdr, z16 (or fmr, z16)
# fhn, fmr?
# jbk, qgq
# tpc, rvf (or pwm, tpc)

# Tried fhn,fmr,jbk,qdr,qgq,rvf,tpc,z16




