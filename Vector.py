# Vector classes for working with coordinates. These are implemented as immutable dataclasses
# so that they can be hashed (stored in sets, etc.).
from dataclasses import dataclass
from typing_extensions import Self

@dataclass(frozen = True)
class Vector:
	x: int
	y: int

	def __add__(self, v: Self) -> Self:
		return type(self)(self.x + v.x, self.y + v.y)

	def __sub__(self, v: Self) -> Self:
		return type(self)(self.x - v.x, self.y - v.y)

	def __neg__(self) -> Self:
		return type(self)(-self.x, -self.y)

	def __mul__(self, c: int) -> Self:
		return type(self)(c * self.x, c * self.y)

	def __rmul__(self, c: int) -> Self:
		return self * c

	def __str__(self) -> str:
		return f"({self.x},{self.y})"

	def in_range(self, xmin: int, xmax: int, ymin: int, ymax: int) -> bool:
		return self.x >= xmin and self.x <= xmax and self.y >= ymin and self.y <= ymax

	def in_range_sq(self, size):
		return self.in_range(0, size - 1, 0, size - 1)

	def rotate_cw(self) -> Self:
		return type(self)(self.y, -self.x)

	def rotate_ccw(self) -> Self:
		return type(self)(-self.y, self.x)

@dataclass(frozen = True)
class Vector3:
	x: int
	y: int
	z: int

	def __add__(self, v: Self) -> Self:
		return type(self)(self.x + v.x, self.y + v.y, self.z + v.z)

	def __sub__(self, v: Self) -> Self:
		return type(self)(self.x - v.x, self.y - v.y, self.z - v.z)

	def __neg__(self) -> Self:
		return type(self)(-self.x, -self.y, -self.z)

	def __mul__(self, c: int) -> Self:
		return type(self)(c * self.x, c * self.y, c * self.z)

	def __rmul__(self, c: int) -> Self:
		return self * c

	def __str__(self) -> str:
		return f"({self.x},{self.y},{self.z})"

	def in_range(self, xmin: int, xmax: int, ymin: int, ymax: int, zmin, zmax) -> bool:
		return self.x >= xmin and self.x <= xmax and self.y >= ymin and self.y <= ymax and self.z >= zmin and self.z <= zmax

	def in_range_sq(self, size):
		return self.in_range(0, size - 1, 0, size - 1, 0, size - 1)
