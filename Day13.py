import re, sys, copy
from collections import namedtuple
from Vector import Vector, up, right

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

# Process the input. It's groups of three lines separated by blank lines. Each group describes
# the movements of a single crane game due to two buttons (A and B) as well as the location of
# a prize.
Machine = namedtuple('Machine', ['a', 'b', 'prize'])

machines_text = input_text.split('\n\n')
machines = []
for machine_text in machines_text:
	nums = [int(n) for n in re.findall(r'\d+', machine_text)]
	machines.append(Machine(Vector(nums[0], nums[1]), Vector(nums[2], nums[3]), Vector(nums[4], nums[5])))

# Part 1: Pressing button A costs 3 tokens and pressing button B costs 1 token. What is the smallest
# number of tokens needed to win all possible prizes? (Not all prizes are winnable!) I checked and
# found that all of the vectors are linearly independent, so I don't think there's actually a
# minimization problem here. We just have to solve a system of equations for each machine and see
# whether there's a solution. To do this, we'll use Cramer's rule, which requires us to calculate
# the determinants of three matrices. Our overall system is:
#
#  |ax bx| |A| = |px|
#  |ay by| |B|   |py|
#
# And the determinants are:
#  |ax bx|  |px bx|  |ax px|
#  |ay by|  |py by|  |ay py|
total = 0
for m in machines:
	detM = m.a.x * m.b.y - m.b.x * m.a.y
	detMa = m.prize.x * m.b.y - m.b.x * m.prize.y
	detMb = m.a.x * m.prize.y - m.prize.x * m.a.y
	A = detMa / detM
	B = detMb / detM
	if A.is_integer() and B.is_integer():
		total += int(3*A + 1*B)

print(f"Part 1: The number of tokens needed to win all possible prizes is: {total}") 

# Part 2: The prizes are now 10000000000000 units farther away in the X and Y directions. Now how
# many tokens does it take to win all possible prizes? The same solution works.
machines = [Machine(m.a, m.b, Vector(m.prize.x + 10000000000000, m.prize.y + 10000000000000)) for m in machines]
total = 0
for m in machines:
	detM = m.a.x * m.b.y - m.b.x * m.a.y
	detMa = m.prize.x * m.b.y - m.b.x * m.prize.y
	detMb = m.a.x * m.prize.y - m.prize.x * m.a.y
	A = detMa / detM
	B = detMb / detM
	if A.is_integer() and B.is_integer():
		total += int(3*A + 1*B)

print(f"Part 2: The number of tokens needed to win all possible prizes is: {total}") 
