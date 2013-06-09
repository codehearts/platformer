from bounded_box import BoundedBox
from pyglet.sprite import Sprite

class ExtendedSprite(Sprite):
	""":class:`pgylet.sprite.Sprite` which tracks its dimensions in terms of pixels and tiles."""

	def __init__(self, *args, **kwargs):
		super(ExtendedSprite, self).__init__(*args, **kwargs)
		self.box = BoundedBox(self._x, self._y, self.width, self.height)

	@property
	def x(self):
		return self.box.x
	@x.setter
	def x(self, x):
		self.box.x = x
		self._set_x(self.box.x)

	@property
	def y(self):
		return self.box.y
	@y.setter
	def y(self, y):
		self.box.y = y
		self._set_y(self.box.y)

	@property
	def x2(self):
		return self.box.x2
	@x2.setter
	def x2(self, x2):
		self.box.x2 = x2
		self._set_x(self.box.x)

	@property
	def y2(self):
		return self.box.y2
	@y2.setter
	def y2(self, y2):
		self.box.y2 = y2
		self._set_y(self.box.y)

	@property
	def x_tile(self):
		return self.box.x_tile
	@x_tile.setter
	def x_tile(self, x_tile):
		self.box.x_tile = x_tile
		self._set_x(self.box.x)

	@property
	def y_tile(self):
		return self.box.y_tile
	@y_tile.setter
	def y_tile(self, y_tile):
		self.box.y_tile = y_tile
		self._set_y(self.box.y)

	@property
	def x2_tile(self):
		return self.box.x2_tile
	@x2_tile.setter
	def x2_tile(self, x2_tile):
		self.box.x2_tile = x2_tile
		self._set_x(self.box.x)

	@property
	def y2_tile(self):
		return self.box.y2_tile
	@y2_tile.setter
	def y2_tile(self, y2_tile):
		self.box.y2_tile = y2_tile
		self._set_y(self.box.y)

	@property
	def tile_x(self):
		return self.box.tile_x
	@tile_x.setter
	def tile_x(self, tile_x):
		self.box.tile_x = tile_x
		self._set_x(self.box.x)

	@property
	def tile_y(self):
		return self.box.tile_y
	@tile_y.setter
	def tile_y(self, tile_y):
		self.box.tile_y = tile_y
		self._set_y(self.box.y)

	@property
	def tile_x2(self):
		return self.box.tile_x2
	@tile_x2.setter
	def tile_x2(self, tile_x2):
		self.box.tile_x2 = tile_x2
		self._set_x(self.box.x)

	@property
	def tile_y2(self):
		return self.box.tile_y2
	@tile_y2.setter
	def tile_y2(self, tile_y2):
		self.box.tile_y2 = tile_y2
		self._set_y(self.box.y)

	@property
	def half_width(self):
		return self.box.half_width

	@property
	def half_height(self):
		return self.box.half_height

	@property
	def tile_width(self):
		return self.box.tile_width

	@property
	def tile_height(self):
		return self.box.tile_height

	@property
	def half_tile_width(self):
		return self.box.half_tile_width

	@property
	def half_tile_height(self):
		return self.box.half_tile_height

	@property
	def tile_width_span(self):
		return self.box.tile_width_span

	@property
	def tile_height_span(self):
		return self.box.tile_height_span
