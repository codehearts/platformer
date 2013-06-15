from settings.general_settings import TILE_SIZE, TILE_SIZE_FLOAT
from math import ceil

# TODO When considering optimization, calling int() and ceil() are slow.
# TODO Are the float tile values necessary?
class BoundedBox(object):
	"""A box which keeps track of its dimensions in terms of pixels and tiles.

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
		tile_x (float): The x coordinate of the box in terms of tiles (as opposed to pixels).
		tile_y (float): The y coordinate of the box in terms of tiles (as opposed to pixels).
		tile_x2 (float): The x2 coordinate of the box in terms of tiles (as opposed to pixels).
		tile_y2 (float): The y2 coordinate of the box in terms of tiles (as opposed to pixels).
		width (int): The width of the box in pixels.
		height (int): The height of the box in pixels.
		half_width (float): Half of the box's width in pixels.
		half_height (float): Half of the box's height in pixels.
		tile_width (float): The width of the box in terms of tiles.
		tile_height (float): The height of the box in terms of tiles.
		half_tile_width (float): Half of the box's width in terms of tiles.
		half_tile_height (float): Half of the box's height in terms of tiles.
		tile_width_span (int): The number of tiles that the box occupies horizontally.
		tile_height_span (int): The number of tiles that the box occupies vertically.
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
		self._height = int(height)
		self._half_height = self._height / 2.0
		self._tile_height = self._height / TILE_SIZE_FLOAT
		self._half_tile_height = self._tile_height / 2.0
		self._tile_height_span = int(ceil(self._tile_height))

		self._width = int(width)
		self._half_width = self._width / 2.0
		self._tile_width = self._width / TILE_SIZE_FLOAT
		self._half_tile_width = self._tile_width / 2.0
		self._tile_width_span = int(ceil(self._tile_width))

		# Setting these properties sets the other coordinates as well
		self.x = x
		self.y = y



	def bound_within(self, box):
		"""Adjusts the dimensions and coordinates of the box to fit within
		the dimensions of another box.

		This is the same as converting this box into the intersection of
		this box and the given box.

		Args:
			box (:class:`game.bounded_box.BoundedBox`): The bounded box to bind this box within.
		"""
		if self._x2 > box.x2:
			self.width = box.x2 - self._x
		if self._x < box.x:
			self.width = self._x2 - box.x
			self.x = box.x

		if self._y2 > box.y2:
			self.height = box.y2 - self._y
		if self._y < box.y:
			self.height = self._y2 - box.y
			self.y = box.y



	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, x):
		x = int(x)
		self._x = x
		self._mid_x = x + int(self._half_width)
		self._x2 = x + self._width
		self._tile_x = x / TILE_SIZE_FLOAT
		self._tile_x2 = self._tile_x + self._tile_width

		self._x_tile = int(self._tile_x)
		if (self._x < 0 and self._x % TILE_SIZE != 0):
			self._x_tile -= 1

		self._mid_x_tile = int(self._tile_x + self._half_tile_width)
		if (self._mid_x > 0 and self._mid_x % TILE_SIZE == 0):
			self._mid_x_tile -= 1
		elif (self._mid_x < 0 and self._mid_x % TILE_SIZE != 0):
			self._mid_x_tile -= 1

		# If the rightmost pixel is divisble by the tile size, our x2_tile
		# will be off by a tile. For example, for a 64px wide object at (0,0)
		# with a 32px tile size, the 64th pixel falls on the 2nd tile, but
		# 64/32 = 2 gives the wrong tile index.
		self._x2_tile = int(self._tile_x2)
		if (self._x2 > 0 and self._x2 % TILE_SIZE == 0):
			self._x2_tile -= 1
		elif (self._x2 < 0):
			self._x2_tile -= 1

	@property
	def y(self):
		"""Gets y."""
		return self._y
	@y.setter
	def y(self, y):
		"""Updates coordinates whenever ``y`` is set."""
		y = int(y)
		self._y = y
		self._mid_y = y + int(self._half_height)
		self._y2 = y + self._height
		self._tile_y = y / TILE_SIZE_FLOAT
		self._tile_y2 = self._tile_y + self._tile_height

		self._y_tile = int(self._tile_y)
		if (self._y < 0 and self._y % TILE_SIZE != 0):
			self._y_tile -= 1

		self._mid_y_tile = int(self._tile_y + self._half_tile_height)
		if (self._mid_y > 0 and self._mid_y % TILE_SIZE == 0):
			self._mid_y_tile -= 1
		elif (self._mid_y < 0 and self._mid_y % TILE_SIZE != 0):
			self._mid_y_tile -= 1

		self._y2_tile = int(self._tile_y2)
		if (self._y2 != 0 and self._y2 % TILE_SIZE == 0):
			self._y2_tile -= 1
		elif (self._y2 < 0):
			self._y2_tile -= 1

	@property
	def mid_x(self):
		"""Gets mid_x."""
		return self._mid_x
	@mid_x.setter
	def mid_x(self, mid_x):
		"""Updates coordinates whenever ``mid_x`` is set."""
		self.x = int(mid_x) - int(self._half_width)

	@property
	def mid_y(self):
		"""Gets mid_y."""
		return self._mid_y
	@mid_y.setter
	def mid_y(self, mid_y):
		"""Updates coordinates whenever ``mid_y`` is set."""
		self.y = int(mid_y) - int(self._half_height)

	@property
	def x2(self):
		"""Gets x2."""
		return self._x2
	@x2.setter
	def x2(self, x2):
		"""Updates coordinates whenever ``x2`` is set."""
		self.x = x2 - self._width

	@property
	def y2(self):
		"""Gets y2."""
		return self._y2
	@y2.setter
	def y2(self, y2):
		"""Updates coordinates whenever ``y2`` is set."""
		self.y = y2 - self._height

	@property
	def x_tile(self):
		"""Gets x_tile."""
		return self._x_tile
	@x_tile.setter
	def x_tile(self, x_tile):
		"""Updates coordinates whenever ``x_tile`` is set."""
		self.x = x_tile * TILE_SIZE

	@property
	def y_tile(self):
		"""Gets y_tile."""
		return self._y_tile
	@y_tile.setter
	def y_tile(self, y_tile):
		"""Updates coordinates whenever ``y_tile`` is set."""
		self.y = y_tile * TILE_SIZE

	@property
	def mid_x_tile(self):
		"""Gets mid_x_tile."""
		return self._mid_x_tile
	@mid_x_tile.setter
	def mid_x_tile(self, mid_x_tile):
		"""Updates coordinates whenever ``mid_x_tile`` is set."""
		self.x = (int(mid_x_tile) - int(self._half_tile_width)) * TILE_SIZE

	@property
	def mid_y_tile(self):
		"""Gets mid_y_tile."""
		return self._mid_y_tile
	@mid_y_tile.setter
	def mid_y_tile(self, mid_y_tile):
		"""Updates coordinates whenever ``mid_y_tile`` is set."""
		self.y = (int(mid_y_tile) - int(self._half_tile_height)) * TILE_SIZE

	@property
	def x2_tile(self):
		"""Gets x2_tile."""
		return self._x2_tile
	@x2_tile.setter
	def x2_tile(self, x2_tile):
		"""Updates coordinates whenever ``x2_tile`` is set."""
		self.x = (x2_tile - self._tile_width) * TILE_SIZE

	@property
	def y2_tile(self):
		"""Gets y2_tile."""
		return self._y2_tile
	@y2_tile.setter
	def y2_tile(self, y2_tile):
		"""Updates coordinates whenever ``y2_tile`` is set."""
		self.y = (y2_tile - self._tile_height) * TILE_SIZE

	@property
	def tile_x(self):
		"""Gets tile_x."""
		return self._tile_x
	@tile_x.setter
	def tile_x(self, tile_x):
		"""Updates coordinates whenever ``tile_x`` is set."""
		self.x = tile_x * TILE_SIZE

	@property
	def tile_y(self):
		"""Gets tile_y."""
		return self._tile_y
	@tile_y.setter
	def tile_y(self, tile_y):
		"""Updates coordinates whenever ``tile_y`` is set."""
		self.y = tile_y * TILE_SIZE

	@property
	def tile_x2(self):
		"""Gets tile_x2."""
		return self._tile_x2
	@tile_x2.setter
	def tile_x2(self, tile_x2):
		"""Updates coordinates whenever ``tile_x2`` is set."""
		self.x = (tile_x2 - self._tile_width) * TILE_SIZE

	@property
	def tile_y2(self):
		"""Gets tile_y2."""
		return self._tile_y2
	@tile_y2.setter
	def tile_y2(self, tile_y2):
		"""Updates coordinates whenever ``tile_y2`` is set."""
		self.y = (tile_y2 - self._tile_height) * TILE_SIZE

	@property
	def width(self):
		"""Gets width."""
		return self._width
	@width.setter
	def width(self, width):
		"""Updates dimensions whenever ``width`` is set."""
		self._width = int(width)
		self._half_width = self._width / 2.0
		self._tile_width = self._width / TILE_SIZE_FLOAT
		self._half_tile_width = self._tile_width / 2.0
		self._tile_width_span = int(ceil(self._tile_width))
		self._mid_x = self._x + int(self._half_width)
		self._x2 = self._x + self._width
		self._tile_x2 = self._tile_x + self._tile_width

		self._mid_x_tile = int(self._tile_x + self._half_tile_width)
		if (self._mid_x > 0 and self._mid_x % TILE_SIZE == 0):
			self._mid_x_tile -= 1
		elif (self._mid_x < 0 and self._mid_x % TILE_SIZE != 0):
			self._mid_x_tile -= 1

		self._x2_tile = int(self._tile_x2)
		if (self._x2 > 0 and self._x2 % TILE_SIZE == 0):
			self._x2_tile -= 1
		elif (self._x2 < 0):
			self._x2_tile -= 1

	@property
	def height(self):
		"""Gets height."""
		return self._height
	@height.setter
	def height(self, height):
		"""Updates dimensions whenever ``height`` is set."""
		self._height = int(height)
		self._half_height = self._height / 2.0
		self._tile_height = self._height / TILE_SIZE_FLOAT
		self._half_tile_height = self._tile_height / 2.0
		self._tile_height_span = int(ceil(self._tile_height))
		self._mid_y = self._y + int(self._half_height)
		self._y2 = self._y + self._height
		self._tile_y2 = self._tile_y + self._tile_height

		self._mid_y_tile = int(self._tile_y + self._half_tile_height)
		if (self._mid_y > 0 and self._mid_y % TILE_SIZE == 0):
			self._mid_y_tile -= 1
		elif (self._mid_y < 0 and self._mid_y % TILE_SIZE != 0):
			self._mid_y_tile -= 1

		self._y2_tile = int(self._tile_y2)
		if (self._y2 > 0 and self._y2 % TILE_SIZE == 0):
			self._y2_tile -= 1
		elif (self._y2 < 0):
			self._y2_tile -= 1

	@property
	def half_width(self):
		return self._half_width
	@half_width.setter
	def half_width(self, half_width):
		self.width = half_width * 2

	@property
	def half_height(self):
		return self._half_height
	@half_height.setter
	def half_height(self, half_height):
		self.height = half_height * 2

	@property
	def tile_width(self):
		"""Gets tile_width."""
		return self._tile_width
	@tile_width.setter
	def tile_width(self, tile_width):
		"""Updates dimensions whenever ``tile_width`` is set."""
		self.width = tile_width * TILE_SIZE

	@property
	def tile_height(self):
		"""Gets tile_height."""
		return self._tile_height
	@tile_height.setter
	def tile_height(self, tile_height):
		"""Updates dimensions whenever ``tile_height`` is set."""
		self.height = tile_height * TILE_SIZE

	@property
	def half_tile_width(self):
		return self._half_tile_width
	@half_tile_width.setter
	def half_tile_width(self, half_tile_width):
		self.width = half_tile_width * TILE_SIZE * 2

	@property
	def half_tile_height(self):
		return self._half_tile_height
	@half_tile_height.setter
	def half_tile_height(self, half_tile_height):
		self.height = half_tile_height * TILE_SIZE * 2

	@property
	def tile_width_span(self):
		"""Gets tile_width_span."""
		return self._tile_width_span
	@tile_width_span.setter
	def tile_width_span(self, tile_width_span):
		"""Updates dimensions whenever ``tile_width_span`` is set."""
		self.width = ceil(tile_width_span) * TILE_SIZE

	@property
	def tile_height_span(self):
		"""Gets tile_height_span."""
		return self._tile_height_span
	@tile_height_span.setter
	def tile_height_span(self, tile_height_span):
		"""Updates dimensions whenever ``tile_height_span`` is set."""
		self.height = ceil(tile_height_span) * TILE_SIZE



	def __eq__(self, other):
		"""Compares this box's x, y, width, and height attributes with those of the other object's."""
		return self._x == other.x and self._y == other.y and self._width == other.width and self._height == other.height
