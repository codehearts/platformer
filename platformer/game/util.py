import math
from settings import general_settings

class Box(object):
	def __init__(self, x, y, width, height):
		self.set(x, y, width, height)

	# @TODO These methods could be optimized

	def set(self, x, y, width, height):
		self.x = int(x)
		self.y = int(y)
		self.width = int(width)
		self.height = int(height)
		self.x2 = self.x + self.width
		self.y2 = self.y + self.height
		self.half_width = self.width / 2
		self.half_height = self.height / 2

	def set_coordinates(self, x, y):
		self.set(x, y, self.width, self.height)

	def set_x(self, x):
		self.set(x, self.y, self.width, self.height)

	def set_y(self, y):
		self.set(self.x, y, self.width, self.height)

	def set_dimensions(self, width, height):
		self.set(self.x, self.y, width, height)

	def set_width(self, width):
		self.set(self.x, self.y, width, self.height)

	def set_height(self, height):
		self.set(self.x, self.y, self.width, height)

class HitBox(Box):
	def __init__(self, x, y, rel_x, rel_y, width, height):
		super(HitBox, self).__init__(x, y, width, height)
		self.rel_x = int(rel_x)
		self.rel_y = int(rel_y)



def distance(point_1 = (0, 0), point_2 = (0, 0)):
	return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

def value_in_range(value, min, max):
	return (value >= min) and (value <= max)

def collision_detected(obj_1, obj_2):
	overlap_x = value_in_range(obj_1.x, obj_2.x, obj_2.x + obj_2.width) or value_in_range(obj_2.x, obj_1.x, obj_1.x + obj_1.width)
	overlap_y = value_in_range(obj_1.y, obj_2.y, obj_2.y + obj_2.height) or value_in_range(obj_2.y, obj_1.y, obj_1.y + obj_1.height)

	return (overlap_x and overlap_y)

def line_intersects_line(l1p1, l1p2, l2p1, l2p2):
	q = (l1p1[1] - l2p1[1]) * (l2p2[0] - l2p1[0]) - (l1p1[0] - l2p1[0]) * (l2p2[1] - l2p1[1])
	d = (l1p2[0] - l1p1[0]) * (l2p2[1] - l2p1[1]) - (l1p2[1] - l1p1[1]) * (l2p2[0] - l2p1[0])

	if d == 0:
		return False

	r = q / d

	q = (l1p1[1] - l2p1[1]) * (l1p2[0] - l1p1[0]) - (l1p1[0] - l2p1[0]) * (l1p2[1] - l1p1[1])
	s = q / d

	if (r < 0 or r > 1 or s < 0 or s > 1):
		return False

	return True

def object_contains_point(obj, p):
	# @TODO Does this even work?
	if (obj.x == p[0] and obj.y == p[1]):
		return True
	elif (obj.x == p[0] and (obj.height+obj.y) == p[1]):
		return True
	elif ((obj.width+obj.x) == p[0] and obj.y == p[1]):
		return True
	elif ((obj.width+obj.x) == p[0] and (obj.height+obj.y) == p[1]):
		return True

	return False

def lies_in_path(obj, p1, p2):
	if line_intersects_line(p1, p2, (obj.x, obj.y), (obj.x + obj.width, obj.y)):
		return True
	elif line_intersects_line(p1, p2, (obj.x + obj.width, obj.y), (obj.x + obj.width, obj.y + obj.height)):
		return True
	elif line_intersects_line(p1, p2, (obj.x + obj.width, obj.y + obj.height), (obj.x, obj.y + obj.height)):
		return True
	elif line_intersects_line(p1, p2, (obj.x, obj.y + obj.height), (obj.x, obj.y)):
		return True

	return (object_contains_point(obj, p1) and object_contains_point(obj, p2))

def get_gravitational_acceleration(mass):
	return -(general_settings.GRAVITY * mass)

def tile_to_coordinate(tile_x, tile_y):
	return (tile_x * general_settings.TILE_SIZE, tile_y * general_settings.TILE_SIZE)

def coordinates_to_tile(x, y):
	return (x / general_settings.TILE_SIZE, y / general_settings.TILE_SIZE)

def coordinate_to_tile(coordinate):
	return coordinate / general_settings.TILE_SIZE


# Makes the second list the same length as the first by repeating it
def equalize_list_sizes(larger_list, smaller_list):
	smaller_size = len(smaller_list)
	new_list = []

	for i in xrange(1, len(larger_list)+1):
		new_list.append(smaller_list[i%smaller_size - 1])

	return new_list

ABS_TOLERANCE = 0.0000000001 # TODO Move this to its own config area
def floats_equal(x, y):
	"""Returns whether two floats are equal within ABS_TOLERANCE."""
	return abs(x - y) <= ABS_TOLERANCE * max(1.0, abs(x), abs(y))
