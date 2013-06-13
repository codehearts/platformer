from bounded_box import BoundedBox
from pyglet.sprite import Sprite

# TODO Write tests to check the position of the sprite object
class ExtendedSprite(Sprite):
	""":class:`pgylet.sprite.Sprite` which tracks its dimensions in terms of pixels and tiles.

	Attributes:
		x (int): The x coordinate of the sprite's anchor point (usually the bottom left corner)
		y (int): The y coordinate of the sprite's anchor point (usually the bottom left corner)
		mid_x (int): The x coordinate of the middle of the box.
		mid_y (int): The y coordinate of the middle of the box.
		x2 (int): The x coordinate of a point opposite the sprite's anchor point (usually the bottom left corner).
		y2 (int): The y coordinate of a point opposite the sprite's anchor point (usually the bottom left corner).
		x_tile (int): The x index of the tile that the sprite's x coordinate is over.
		y_tile (int): The y index of the tile that the sprite's y coordinate is over.
		mid_x_tile (int): The x index of the tile that the middle of the box is over.
		mid_y_tile (int): The y index of the tile that the middle of the box is over.
		x2_tile (int): The x index of the tile that the sprite's x2 coordinate is over.
		y2_tile (int): The y index of the tile that the sprite's y2 coordinate is over.
		tile_x (float): The x coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_y (float): The y coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_x2 (float): The x2 coordinate of the sprite in terms of tiles (as opposed to pixels).
		tile_y2 (float): The y2 coordinate of the sprite in terms of tiles (as opposed to pixels).
		width (int): The width of the sprite in pixels.
		height (int): The height of the sprite in pixels.
		half_width (int): Half of the sprite's width in pixels.
		half_height (int): Half of the sprite's height in pixels.
		tile_width (float): The width of the sprite in terms of tiles.
		tile_height (float): The height of the sprite in terms of tiles.
		half_tile_width (float): Half of the sprite's width in terms of tiles.
		half_tile_height (float): Half of the sprite's height in terms of tiles.
		tile_width_span (int): The number of tiles that the sprite occupies horizontally.
		tile_height_span (int): The number of tiles that the sprite occupies vertically.
	"""

	def __init__(self, *args, **kwargs):
		super(ExtendedSprite, self).__init__(*args, **kwargs)

		self._width = int(self._texture.width * self._scale)
		self._height = int(self._texture.height * self._scale)

		self.box = BoundedBox(self._x, self._y, self._width, self._height)

	def _set_sprite_x(self, x):
		self.box.x = x
		self._set_x(self.box.x)

	def _set_sprite_mid_x(self, mid_x):
		self.box.mid_x = mid_x
		self._set_x(self.box.x)

	def _set_sprite_x2(self, x2):
		self.box.x2 = x2
		self._set_x(self.box.x)

	def _set_sprite_x_tile(self, x_tile):
		self.box.x_tile = x_tile
		self._set_x(self.box.x)

	def _set_sprite_mid_x_tile(self, mid_x_tile):
		self.box.mid_x_tile = mid_x_tile
		self._set_x(self.box.x)

	def _set_sprite_x2_tile(self, x2_tile):
		self.box.x2_tile = x2_tile
		self._set_x(self.box.x)

	def _set_sprite_tile_x(self, tile_x):
		self.box.tile_x = tile_x
		self._set_x(self.box.x)

	def _set_sprite_tile_x2(self, tile_x2):
		self.box.tile_x2 = tile_x2
		self._set_x(self.box.x)

	x = property(lambda self: self.box.x, _set_sprite_x)
	mid_x = property(lambda self: self.box.mid_x, _set_sprite_mid_x)
	x2 = property(lambda self: self.box.x2, _set_sprite_x2)
	x_tile = property(lambda self: self.box.x_tile, _set_sprite_x_tile)
	mid_x_tile = property(lambda self: self.box.mid_x_tile, _set_sprite_mid_x_tile)
	x2_tile = property(lambda self: self.box.x2_tile, _set_sprite_x2_tile)
	tile_x = property(lambda self: self.box.tile_x, _set_sprite_tile_x)
	tile_x2 = property(lambda self: self.box.tile_x2, _set_sprite_tile_x2)


	def _set_sprite_y(self, y):
		self.box.y = y
		self._set_y(self.box.y)

	def _set_sprite_mid_y(self, mid_y):
		self.box.mid_y = mid_y
		self._set_y(self.box.y)

	def _set_sprite_y2(self, y2):
		self.box.y2 = y2
		self._set_y(self.box.y)

	def _set_sprite_y_tile(self, y_tile):
		self.box.y_tile = y_tile
		self._set_y(self.box.y)

	def _set_sprite_mid_y_tile(self, mid_y_tile):
		self.box.mid_y_tile = mid_y_tile
		self._set_y(self.box.y)

	def _set_sprite_y2_tile(self, y2_tile):
		self.box.y2_tile = y2_tile
		self._set_y(self.box.y)

	def _set_sprite_tile_y(self, tile_y):
		self.box.tile_y = tile_y
		self._set_y(self.box.y)

	def _set_sprite_tile_y2(self, tile_y2):
		self.box.tile_y2 = tile_y2
		self._set_y(self.box.y)

	y = property(lambda self: self.box.y, _set_sprite_y)
	mid_y = property(lambda self: self.box.mid_y, _set_sprite_mid_y)
	y2 = property(lambda self: self.box.y2, _set_sprite_y2)
	y_tile = property(lambda self: self.box.y_tile, _set_sprite_y_tile)
	mid_y_tile = property(lambda self: self.box.mid_y_tile, _set_sprite_mid_y_tile)
	y2_tile = property(lambda self: self.box.y2_tile, _set_sprite_y2_tile)
	tile_y = property(lambda self: self.box.tile_y, _set_sprite_tile_y)
	tile_y2 = property(lambda self: self.box.tile_y2, _set_sprite_tile_y2)


	@property
	def half_width(self):
		return self.box.half_width
	@property
	def tile_width(self):
		return self.box.tile_width
	@property
	def half_tile_width(self):
		return self.box.half_tile_width
	@property
	def tile_width_span(self):
		return self.box.tile_width_span


	@property
	def half_height(self):
		return self.box.half_height
	@property
	def tile_height(self):
		return self.box.tile_height
	@property
	def half_tile_height(self):
		return self.box.half_tile_height
	@property
	def tile_height_span(self):
		return self.box.tile_height_span
