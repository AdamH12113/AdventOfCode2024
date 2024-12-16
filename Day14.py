import re, sys, copy, os
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

# Process the input. Each line gives the position and velocity of a robot. We're also given an area
# size that differs between the example and the real input.
xsize, ysize = (11, 7) if '--example' in sys.argv else (101, 103)

Robot = namedtuple('Robot', ['p', 'v'])
robots = []
for line in input_text.split('\n'):
	nums = [int(n) for n in re.findall(r'-?\d+', line)]
	new_robot = Robot(nums[0]*right + nums[1]*up, nums[2]*right + nums[3]*up)
	robots.append(new_robot)

# Part 1: After 100 seconds, count the number of robots in each quadrant and multiply the counts.
# The area wraps around at the edges, so the robots "teleport" when they cross an edge. Python's
# standard modulus division works exactly the way we need for this.
def update_robot(robot, seconds):
	mx = robot.p.x + seconds*robot.v.x
	my = robot.p.y + seconds*robot.v.y
	return Robot(Vector(mx % xsize, my % ysize), robot.v)

def score_robots(robots):
	qul = 0
	qur = 0
	qbl = 0
	qbr = 0
	for robot in robots:
		if robot.p.x < xsize // 2:
			if robot.p.y < ysize // 2:
				qbl += 1
			elif robot.p.y > ysize // 2:
				qul += 1
		elif robot.p.x > xsize // 2:
			if robot.p.y < ysize // 2:
				qbr += 1
			elif robot.p.y > ysize // 2:
				qur += 1
	return qul * qur * qbl * qbr

moved_robots = [update_robot(r, 100) for r in robots]
score = score_robots(moved_robots)
print(f"Part 1: The safety score is: {score}")

# Part 2: How many seconds will it take for the robots to arrange themselves into a Christmas tree?
# The usual way people do this is by searching for symmetry or grouping in the coordinates but in
# my opinion requiring a *visual* condition makes this inherently a bad puzzle. Someone online said
# that looking for the minimum safety factor is a good idea. Printing the grid every time I find a
# new minimum safety factor found me the right time, which was 6475.
def print_robots(robots):
	grid = [['.' for x in range(xsize)] for y in range(ysize)]
	for r in robots:
		grid[r.p.y][r.p.x] = '#'

	for y in range(ysize):
		for x in range(xsize):
			print(grid[y][x], end='')
		print()
	print()

print_robots([update_robot(r, 6475) for r in robots])

#moved_robots = robots
#min_score = 99999999999
#for t in range(1, 10000+1):
#	moved_robots = [update_robot(r, 1) for r in moved_robots]
#	score = score_robots(moved_robots)
#	if score < min_score:
#		min_score = score
#		print_robots(moved_robots)
#		print(f"New min: t={t}  score={score}")
