from pyglet.sprite import Sprite
from settings.general_settings import TILE_SIZE
import math

class ExtendedSprite(Sprite):
	""":class:`pgylet.sprite.Sprite` with additional attributes.

	Attributes:
		x (int): The x coordinate of the sprite's anchor point (usually the bottom left corner)
		y (int): The y coordinate of the sprite's anchor point (usually the bottom left corner)
		x2 (int): The x coordinate of a point opposite the sprite's anchor point (usually the bottom left corner).
		y2 (int): The y coordinate of a point opposite the sprite's anchor point (usually the bottom left corner).
		tile_x (int): The x coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_y (int): The y coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_x2 (int): The x2 coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_y2 (int): The y2 coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_width (int): The number of tiles that the sprite occupies horizontally.
		tile_height (int): The number of tiles that the sprite occupies vertically.
	"""

	def __init__(self, *args, **kwargs):
		super(ExtendedSprite, self).__init__(*args, **kwargs)

		self.tile_width = math.ceil(self.width / TILE_SIZE)
		self.tile_height = math.ceil(self.height / TILE_SIZE)

		# Setting these properties sets the other coordinates as well
		self.x = self.x
		self.y = self.y

	@Sprite.x.setter
	def x(self, x):
		"""Updates coordinates whenever ``x`` is set."""
		x = int(x)
		self._x = x
		self._x2 = x + self.width
		self._tile_x = x / TILE_SIZE
		self._tile_x2 = self._tile_x + self.tile_width

	@Sprite.y.setter
	def y(self, y):
		"""Updates coordinates whenever ``y`` is set."""
		y = int(y)
		self._y = y
		self._y2 = y + self.height
		self._tile_y = y / TILE_SIZE
		self._tile_y2 = self._tile_y + self.tile_height

	@property
	def x2(self):
		"""Gets x2."""
		return self._x2

	@x2.setter
	def x2(self, x2):
		"""Updates coordinates whenever ``x2`` is set."""
		self.x = x2 - self.width

	@property
	def y2(self):
		"""Gets y2."""
		return self._y2

	@y2.setter
	def y2(self, y2):
		"""Updates coordinates whenever ``y2`` is set."""
		self.y = y2 - self.height

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
		self.x = (tile_x2 - self.tile_width) * TILE_SIZE

	@property
	def tile_y2(self):
		"""Gets tile_y2."""
		return self._tile_y2

	@tile_y2.setter
	def tile_y2(self, tile_y2):
		"""Updates coordinates whenever ``tile_y2`` is set."""
		self.y = (tile_y2 - self.tile_height) * TILE_SIZE
