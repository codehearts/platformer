from settings.general_settings import TILE_SIZE, TILE_SIZE_FLOAT
from math import ceil

class BoundedBox(object):
	"""A box which keeps track of its position and dimensions in terms of pixels and tiles.

	Attributes:
		x (int): The x coordinate of the box's anchor point (usually the bottom left corner)
		y (int): The y coordinate of the box's anchor point (usually the bottom left corner)
		mid_x (int): The x coordinate of the middle of the box.
		mid_y (int): The y coordinate of the middle of the box.
		x2 (int): The x coordinate of a point opposite the box's anchor point (usually the bottom left corner).
		y2 (int): The y coordinate of a point opposite the box's anchor point (usually the bottom left corner).
		x_tile (int): The x index of the tile that the box's x coordinate is over.
		y_tile (int): The y index of the tile that the box's y coordinate is over.
		mid_x_tile (int): The x index of the tile that the middle of the box is over.
		mid_y_tile (int): The y index of the tile that the middle of the box is over.
		x2_tile (int): The x index of the tile that the box's x2 coordinate is over.
		y2_tile (int): The y index of the tile that the box's y2 coordinate is over.
		width (int): The width of the box in pixels.
		height (int): The height of the box in pixels.
		half_width (float): Half of the box's width in pixels.
		half_height (float): Half of the box's height in pixels.
		tile_width (int): The number of tiles that the box occupies horizontally.
		tile_height (int): The number of tiles that the box occupies vertically.
		half_tile_width (float): Half of the box's width in terms of tiles.
		half_tile_height (float): Half of the box's height in terms of tiles.
	"""

	def __init__(self, x, y, width, height):
		"""Creates a new bounded box.

		Args:
			x (int): The x coordinate of the box.
			y (int): The y coordinate of the box.
			width (int): The width of the box.
			height (int): The height of the box.
		"""
		# Set the initial dimensions before setting coordinates
		self._height      = int(height)
		self._half_height = self._height / 2.0

		self._tile_height_float = self._height / TILE_SIZE_FLOAT
		self._half_tile_height  = self._tile_height_float / 2.0

		self._half_tile_height_int = int(self._half_tile_height)
		self._half_height_int      = int(self._half_height)

		self._tile_height = int(ceil(self._tile_height_float))


		self._width      = int(width)
		self._half_width = self._width / 2.0

		self._tile_width_float = self._width / TILE_SIZE_FLOAT
		self._half_tile_width  = self._tile_width_float / 2.0

		self._half_tile_width_int = int(self._half_tile_width)
		self._half_width_int      = int(self._half_width)

		self._tile_width = int(ceil(self._tile_width_float))


		# Set the coordinates
		self._set_x(x)
		self._set_y(y)



	def get_intersection(self, box):
		"""Returns the intersection of this box and another box.

		If the boxes do not overlap, ``None`` will be returned.

		Args:
			box (:class:`game.bounded_box.BoundedBox`): The bounded box to intersect with.

		Returns:
			A :class:`game.bounded_box.BoundedBox` of the intersection region, or ``None`` if there was no intersection.
		"""
		intersection = BoundedBox(self._x, self._y, self._width, self._height)

		if self._x2 > box.x2:
			intersection._set_width(max(box.x2 - self._x, 0))
		if intersection._x < box.x:
			intersection._set_width(max(intersection._x2 - box.x, 0))
			intersection._set_x(box.x)

		# No overlap in this case
		if intersection._width == 0:
			return None

		if self._y2 > box.y2:
			intersection._set_height(max(box.y2 - self._y, 0))
		if intersection._y < box.y:
			intersection._set_height(max(intersection._y2 - box.y, 0))
			intersection._set_y(box.y)

		# No overlap in this case
		if intersection._height == 0:
			return None

		return intersection



	def bound_within(self, bounding_box):
		"""Bounds this box within the given bounding box.

		This box's coordinates will be adjusted to remain inside the bounding box.
		It is the programmer's job to ensure that the bounding box is not smaller than this box.

		Args:
			bounding_box (:class:`game.bounded_box.BoundedBox`): The box to bound within.
		"""
		if self._x < bounding_box.x:
			self._set_x(bounding_box.x)
		elif self._x2 > bounding_box.x2:
			self._set_x(bounding_box.x2 - self._width)

		if self._y < bounding_box.y:
			self._set_y(bounding_box.y)
		elif self._y2 > bounding_box.y2:
			self._set_y(bounding_box.y2 - self._height)

		return self



	def _set_x(self, x):
		"""Positions the box to have its lower left corner on the specified coordinate."""
		x = int(x)

		self._x     = x
		self._mid_x = x + self._half_width_int
		self._x2    = x + self._width

		self._x_tile_float  = x / TILE_SIZE_FLOAT
		self._x2_tile_float = self._x_tile_float + self._tile_width_float

		self._x_tile = int(self._x_tile_float)
		if (self._x < 0 and self._x % TILE_SIZE != 0):
			self._x_tile -= 1

		self._mid_x_tile = int(self._x_tile_float + self._half_tile_width)
		if (self._mid_x > 0 and self._mid_x % TILE_SIZE == 0):
			self._mid_x_tile -= 1
		elif (self._mid_x < 0 and self._mid_x % TILE_SIZE != 0):
			self._mid_x_tile -= 1

		# If the rightmost pixel is divisible by the tile size, our x2_tile
		# will be off by a tile. For example, for a 64px wide object at (0,0)
		# with a 32px tile size, the 64th pixel falls on the 2nd tile, but
		# 64/32 = 2 gives the wrong tile index.
		self._x2_tile = int(self._x2_tile_float)
		if ((self._x2 > 0 and self._x2 % TILE_SIZE == 0) or self._x2 < 0):
			self._x2_tile -= 1

	x = property(lambda self: self._x, _set_x)


	def _set_y(self, y):
		"""Positions the box to have its lower left corner on the specified coordinate."""
		y = int(y)

		self._y     = y
		self._mid_y = y + self._half_height_int
		self._y2    = y + self._height

		self._y_tile_float  = y / TILE_SIZE_FLOAT
		self._y2_tile_float = self._y_tile_float + self._tile_height_float

		self._y_tile = int(self._y_tile_float)
		if (self._y < 0 and self._y % TILE_SIZE != 0):
			self._y_tile -= 1

		self._mid_y_tile = int(self._y_tile_float + self._half_tile_height)
		if (self._mid_y > 0 and self._mid_y % TILE_SIZE == 0):
			self._mid_y_tile -= 1
		elif (self._mid_y < 0 and self._mid_y % TILE_SIZE != 0):
			self._mid_y_tile -= 1

		self._y2_tile = int(self._y2_tile_float)
		if ((self._y2 != 0 and self._y2 % TILE_SIZE == 0) or self._y2 < 0):
			self._y2_tile -= 1

	y = property(lambda self: self._y, _set_y)


	def _set_mid_x(self, mid_x):
		self._set_x(int(mid_x) - self._half_width_int)
	mid_x = property(lambda self: self._mid_x, _set_mid_x)

	def _set_mid_y(self, mid_y):
		self._set_y(int(mid_y) - self._half_height_int)
	mid_y = property(lambda self: self._mid_y, _set_mid_y)


	def _set_x2(self, x2):
		self._set_x(x2 - self._width)
	x2 = property(lambda self: self._x2, _set_x2)

	def _set_y2(self, y2):
		self._set_y(y2 - self._height)
	y2 = property(lambda self: self._y2, _set_y2)


	def _set_x_tile(self, x_tile):
		self._set_x(x_tile * TILE_SIZE)
	x_tile = property(lambda self: self._x_tile, _set_x_tile)

	def _set_y_tile(self, y_tile):
		self._set_y(y_tile * TILE_SIZE)
	y_tile = property(lambda self: self._y_tile, _set_y_tile)


	def _set_mid_x_tile(self, mid_x_tile):
		self._set_x((int(mid_x_tile) - self._half_tile_width_int) * TILE_SIZE)
	mid_x_tile = property(lambda self: self._mid_x_tile, _set_mid_x_tile)

	def _set_mid_y_tile(self, mid_y_tile):
		self._set_y((int(mid_y_tile) - self._half_tile_height_int) * TILE_SIZE)
	mid_y_tile = property(lambda self: self._mid_y_tile, _set_mid_y_tile)


	def _set_x2_tile(self, x2_tile):
		self._set_x((x2_tile - self._tile_width_float) * TILE_SIZE)
	x2_tile = property(lambda self: self._x2_tile, _set_x2_tile)

	def _set_y2_tile(self, y2_tile):
		self._set_y((y2_tile - self._tile_height_float) * TILE_SIZE)
	y2_tile = property(lambda self: self._y2_tile, _set_y2_tile)




	def _set_width(self, width):
		"""Sets the box's width."""
		self._width      = int(width)
		self._half_width = self._width / 2.0

		self._tile_width_float = self._width / TILE_SIZE_FLOAT
		self._half_tile_width  = self._tile_width_float / 2.0

		self._half_tile_width_int = int(self._half_tile_width)
		self._half_width_int      = int(self._half_width)

		self._tile_width = int(ceil(self._tile_width_float))

		self._mid_x         = self._x + self._half_width_int
		self._x2            = self._x + self._width
		self._x2_tile_float = self._x_tile_float + self._tile_width_float

		self._mid_x_tile = int(self._x_tile_float + self._half_tile_width)
		if (self._mid_x > 0 and self._mid_x % TILE_SIZE == 0):
			self._mid_x_tile -= 1
		elif (self._mid_x < 0 and self._mid_x % TILE_SIZE != 0):
			self._mid_x_tile -= 1

		self._x2_tile = int(self._x2_tile_float)
		if ((self._x2 > 0 and self._x2 % TILE_SIZE == 0) or self._x2 < 0):
			self._x2_tile -= 1

	width = property(lambda self: self._width, _set_width)


	def _set_height(self, height):
		"""Sets the box's height."""
		self._height      = int(height)
		self._half_height = self._height / 2.0

		self._tile_height_float = self.height / TILE_SIZE_FLOAT
		self._half_tile_height  = self._tile_height_float / 2.0

		self._half_tile_height_int = int(self._half_tile_height)
		self._half_height_int      = int(self._half_height)

		self._tile_height = int(ceil(self._tile_height_float))

		self._mid_y         = self._y + self._half_height_int
		self._y2            = self._y + self._height
		self._y2_tile_float = self._y_tile_float + self._tile_height_float

		self._mid_y_tile = int(self._y_tile_float + self._half_tile_height)
		if (self._mid_y > 0 and self._mid_y % TILE_SIZE == 0):
			self._mid_y_tile -= 1
		elif (self._mid_y < 0 and self._mid_y % TILE_SIZE != 0):
			self._mid_y_tile -= 1

		self._y2_tile = int(self._y2_tile_float)
		if ((self._y2 > 0 and self._y2 % TILE_SIZE == 0) or self._y2 < 0):
			self._y2_tile -= 1

	height = property(lambda self: self._height, _set_height)


	def _set_tile_width(self, tile_width):
		self._set_width(ceil(tile_width) * TILE_SIZE)
	tile_width = property(lambda self: self._tile_width, _set_tile_width)

	def _set_tile_height(self, tile_height):
		self.height = ceil(tile_height) * TILE_SIZE
	tile_height = property(lambda self: self._tile_height, _set_tile_height)


	@property
	def half_width(self):
		return self._half_width
	@property
	def half_height(self):
		return self._half_height


	@property
	def half_tile_width(self):
		return self._half_tile_width
	@property
	def half_tile_height(self):
		return self._half_tile_height



	def __eq__(self, other):
		"""Compares this box's x, y, width, and height attributes with those of the other object's."""
		return self._x == other.x and self._y == other.y and self._width == other.width and self._height == other.height
