from settings.general_settings import TILE_SIZE, TILE_SIZE_FLOAT

class BoundedBox(object):
	"""A box which keeps track of its dimensions in terms of pixels and tiles.

	Attributes:
		x (int): The x coordinate of the box's anchor point (usually the bottom left corner)
		y (int): The y coordinate of the box's anchor point (usually the bottom left corner)
		x2 (int): The x coordinate of a point opposite the box's anchor point (usually the bottom left corner).
		y2 (int): The y coordinate of a point opposite the box's anchor point (usually the bottom left corner).
		tile_x (int): The x coordinate of the box in terms of tiles (as opposed to pixels).
		tile_y (int): The y coordinate of the box in terms of tiles (as opposed to pixels).
		tile_x2 (int): The x2 coordinate of the box in terms of tiles (as opposed to pixels).
		tile_y2 (int): The y2 coordinate of the box in terms of tiles (as opposed to pixels).
		width (int): The width of the box in pixels.
		height (int): The height of the box in pixels.
		tile_width (int): The number of tiles that the box occupies horizontally.
		tile_height (int): The number of tiles that the box occupies vertically.
	"""

	def __init__(self, x, y, width, height):
		"""Creates a new bounded box.

		Args:
			x (int): The x coordinate of the box.
			y (int): The y coordinate of the box.
			width (int): The width of the box.
			height (int): The height of the box.
		"""
		# Set the initial dimenions before setting coordinates
		self._height = int(height)
		self._tile_height = height / TILE_SIZE_FLOAT
		self._width = int(width)
		self._tile_width = width / TILE_SIZE_FLOAT

		# Setting these properties sets the other coordinates as well
		self.x = x
		self.y = y

	@property
	def x(self):
		"""Gets x."""
		return self._x

	@x.setter
	def x(self, x):
		"""Updates coordinates whenever ``x`` is set."""
		x = int(x)
		self._x = x
		self._x2 = x + self._width
		self._tile_x = x / TILE_SIZE_FLOAT
		self._tile_x2 = self._tile_x + self._tile_width

	@property
	def y(self):
		"""Gets y."""
		return self._y

	@y.setter
	def y(self, y):
		"""Updates coordinates whenever ``y`` is set."""
		y = int(y)
		self._y = y
		self._y2 = y + self._height
		self._tile_y = y / TILE_SIZE_FLOAT
		self._tile_y2 = self._tile_y + self._tile_height

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
		self._tile_width = width / TILE_SIZE_FLOAT
		self._x2 = self._x + self._width
		self._tile_x2 = self._tile_x + self._tile_width

	@property
	def height(self):
		"""Gets height."""
		return self._height

	@height.setter
	def height(self, height):
		"""Updates dimensions whenever ``height`` is set."""
		self._height = int(height)
		self._tile_height = height / TILE_SIZE_FLOAT
		self._y2 = self._y + self._height
		self._tile_y2 = self._tile_y + self._tile_height

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
