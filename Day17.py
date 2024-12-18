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

# Process the input. Today we're doing a machine code interpreter, so there are three starting
# register states and a list of opcodes and operands, all integral.
start_a = int(re.findall(r'Register A: \d+', input_text)[0].split(': ')[1])
start_b = int(re.findall(r'Register B: \d+', input_text)[0].split(': ')[1])
start_c = int(re.findall(r'Register C: \d+', input_text)[0].split(': ')[1])
program_text = input_text.split('\n\n')[1]
program = [int(n) for n in re.findall(r'\d+', program_text)]

# Part 1: Concatenate the output values. What is the result?
class Computer:
	def __init__(self, program, start_a, start_b, start_c):
		self.program = copy.deepcopy(program)
		self.a = start_a
		self.b = start_b
		self.c = start_c
		self.ip = 0
		self.output = []
	
	def combo_operand(self, n):
		if n <= 3:
			return n
		elif n == 4:
			return self.a
		elif n == 5:
			return self.b
		elif n == 6:
			return self.c
	
	def adv(self, n):
		self.a = self.a // (2 ** self.combo_operand(n))
		self.ip += 2
	
	def bxl(self, n):
		self.b = self.b ^ n
		self.ip += 2
	
	def bst(self, n):
		self.b = self.combo_operand(n) % 8
		self.ip += 2
	
	def jnz(self, n):
		if self.a == 0:
			self.ip += 2
		else:
			self.ip = n
	
	def bxc(self, n):
		self.b = self.b ^ self.c
		self.ip += 2
	
	def out(self, n):
		self.output.append(self.combo_operand(n) % 8)
		self.ip += 2

	def bdv(self, n):
		self.b = self.a // (2 ** self.combo_operand(n))
		self.ip += 2
	
	def cdv(self, n):
		self.c = self.a // (2 ** self.combo_operand(n))
		self.ip += 2
	def run_operation(self):
		operator = program[self.ip]
		operand = program[self.ip + 1]
		if operator == 0:
			self.adv(operand)
		elif operator == 1:
			self.bxl(operand)
		elif operator == 2:
			self.bst(operand)
		elif operator == 3:
			self.jnz(operand)
		elif operator == 4:
			self.bxc(operand)
		elif operator == 5:
			self.out(operand)
		elif operator == 6:
			self.bdv(operand)
		elif operator == 7:
			self.cdv(operand)
	
	def run_program(self):
		while self.ip < len(program):
			self.run_operation()

comp = Computer(program, start_a, start_b, start_c)
comp.run_program()
print(f"Part 1: The concatenated output is: {','.join(str(n) for n in comp.output)}")

# Part 2: Find an initialization value for register A that causes the program to output a copy
# of itself. The example's answer is 117440, so the search might take a while. To optimize this,
# we'll keep track of the output as the program progresses and abort a run as soon as it produces
# an incorrect value.
#
# No luck. Looking online, it seems like the only way to solve this is through inspection of the
# program, which is a bit disappointing. It turns out that the last output digit is only affected
# by the highest octal digit of the input. The next-to-last output digit is affected by the highest
# and second-highest input digits, and so on. Thus, we need to do a recursive search based on the
# highest unresolved output digit.
def find_init_value(digit, current_init_value):
	for d in range(8):
		test_init = current_init_value + d * 8**digit
		comp = Computer(program, test_init, start_b, start_c)
		comp.run_program()
		if comp.output[digit:] == program[digit:]:
			if digit == 0:
				return test_init
			final_init = find_init_value(digit - 1, test_init)
			if final_init != -1:
				return final_init
	return -1

init_value = find_init_value(len(program) - 1, 0)
print(f"Part 2: The correct initialization value is: {init_value}")
