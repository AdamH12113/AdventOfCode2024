import re, sys, copy
from dataclasses import dataclass, field
from Vector import Vector, up, down, left, right, upleft, upright, downleft, downright

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

# Process the input. It's a 2D grid where each cell is a letter that indicates a type of garden plot.
grid = list(reversed(input_text.split('\n')))
size = len(grid)
plots = {Vector(x, y): grid[y][x] for x in range(size) for y in range(size)}

# Part 1: Find the total price of fencing all the regions. The price of one region is the area of the
# region times its perimeter. Critically, letters can be reused in unconnected regions, which need to
# be distinguished from each other.
outer_perimeters: dict[Vector, int] = {}
checked: set[Vector] = set()
@dataclass
class Region:
	letter: str
	plots: set[Vector] = field(default_factory = set)

regions: list[Region] = []

for x in range(size):
	for y in range(size):
		c = Vector(x, y)
		if c not in checked:
			plot_type = plots[c]
			region = Region(plot_type)
			queue = [c]
			visited = set()
			while len(queue) > 0:
				plot = queue.pop()
				visited.add(plot)
				checked.add(plot)
				region.plots.add(plot)
				outer_perimeters[plot] = 0
				for neighbor in (plot + up, plot + down, plot + left, plot + right):
					if neighbor in plots and plots[neighbor] == plot_type:
						if not neighbor in visited and not neighbor in queue:
							queue.insert(0, neighbor)
					else:
						outer_perimeters[plot] += 1
			regions.append(region)

total_price = sum((len(region.plots) * sum(outer_perimeters[plot] for plot in region.plots)) for region in regions)
print(f"Part 1: The total price of all regions is: {total_price}")
				
# Part 2: Instead of using the perimeter, the price is now based on the number of sides the region has.
# Regions can have holes, so there may be sides on the inside as well as the outside! Counting sides is
# hard, but I'm pretty sure the number of sides is equal to the number of corners. Counting corners is
# easy! (Hopefully.) Let's enumerate the types of corners:
#
#   AAAa*    Simple outer corner: 5 non-neighbors, all adjacent
#   AAAA
#   AAAA
#   AAAA
#
#   AA       Simple inner corner: 1 non-neighbor, diagonal
#   AA* 
#   AaAA
#   AAAA
#
#    ~       Outer protrusion (double corner): 5 non-neighbors, all adjacent
#    a
#   AAAA
#   AAAA
#
#   AA A     Inner protrusion (double corner): 1 non-neighbor, vertical or horizontal
#   AA~A
#   AAaA
#   AAAA
#
#   AAA*     Outer/inner double corner: 2 non-neighbors, diagonal
#   AAaA
#    *AA
#     AA
#
# Crud, this is getting complicated. Finding single corners is easy but double corners have a lot
# of configurations. We need a simpler scheme. Okay, how about this: do differing opposite-side
# neighbors indicate a corner? And would multiple such pairs indicate multiple corners? Better idea:
# Go around the neighboring plots and see when we switch from neighbor to non-neighbor across a
# diagonal. Each switch is one corner.
#
# Nope, that doesn't work either. Regions with diagonally-adjacent corners complicate things. How
# about combining the two approaches? Look for patterns of switches -- four each for outer corners
# and inner corners. That covers protrusions too. I can define sequences of neighbors and whether
# or not they should be in or out of the region.
outer_corner_steps_groups = ((left, up), (up, right), (right, down), (down, left))
outer_corner_match = (False, False)
inner_corner_steps_groups = ((left, upleft, up), (up, upright, right), (right, downright, down), (down, downleft, left))
inner_corner_match = (True, False, True)

def count_region_corners(region):
	region_corners = 0
	for plot in region.plots:
		plot_corners = 0
		for corner_steps in outer_corner_steps_groups:
			if all((plot + corner_steps[s] in region.plots) == outer_corner_match[s] for s in range(len(corner_steps))):
				plot_corners += 1
		for corner_steps in inner_corner_steps_groups:
			if all((plot + corner_steps[s] in region.plots) == inner_corner_match[s] for s in range(len(corner_steps))):
				plot_corners += 1
		region_corners += plot_corners
	return region_corners

total_price = sum((len(region.plots) * count_region_corners(region)) for region in regions)
print(f"Part 2: The total price of all regions is: {total_price}")
