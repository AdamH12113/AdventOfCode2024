import re, sys, copy, os
from collections import namedtuple
from Vector import Vector, up, down, left, right

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

# Process the input. It's a list of 2D coordinates where bytes will obstruct the path through a
# 71x71 (in the real input) or 7x7 (in the example) grid.
start = Vector(0, 0)
size = 7 if '--example' in sys.argv else 71
exit = Vector(size - 1, size - 1)
incoming_bytes = []
for line in input_text.split('\n'):
	nums = [int(n) for n in line.split(',')]
	incoming_bytes.append(Vector(nums[0], nums[1]))

# Part 1: After the first 1024 bytes (for the real input) or 12 bytes (in the example) have fallen,
# what is the smallest number of steps it takes to reach the exit? Time for another BFS!
QueueEntry = namedtuple('QueueEntry', ['coords', 'steps'])

bytes = set(incoming_bytes[:12 if '--example' in sys.argv else 1024])
visited = {}
queue = [QueueEntry(start, 0)]
while len(queue) > 0:
	node = queue.pop()
	if node.coords not in visited or node.steps < visited[node.coords]:
		visited[node.coords] = node.steps
		for dir in (up, down, left, right):
			nc = node.coords + dir
			if nc.in_range_sq(size) and nc not in bytes and (nc not in visited or visited[nc] > node.steps + 1):
				queue.insert(0, QueueEntry(nc, node.steps + 1))

print(f"Part 1: The smallest number of steps needed to reach the exit is: {visited[exit]}")

# Part 2: What are the coordinates of the first byte that will prevent the exit from being
# reachable? There are only a few thousand bytes, so I think we can just iterate this. A binary
# search would be much faster, but I'm tired today.
def exit_is_reachable(num_bytes):
	bytes = set(incoming_bytes[:num_bytes])
	visited = set()
	queue = [start]
	while len(queue) > 0:
		node = queue.pop()
		if node not in visited:
			visited.add(node)
			for dir in (up, down, left, right):
				nc = node + dir
				if nc == exit:
					return True
				if nc.in_range_sq(size) and nc not in bytes and nc not in visited:
					queue.insert(0, nc)
	return exit in visited

for nb in range(len(incoming_bytes)):
	if not exit_is_reachable(nb):
		byte = incoming_bytes[nb - 1]
		print(f"Part 2: The first byte that blocks the exit is: {byte.x},{byte.y}")
		break







