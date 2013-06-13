from physical_object import PhysicalObject
from game.bounded_box import BoundedBox

class HitboxPhysicalObject(PhysicalObject):

	def __init__(self, *args, **kwargs):
		super(HitboxPhysicalObject, self).__init__(*args, **kwargs)
		# TODO The hitbox class could be a more lightweight class
		self.hitbox = BoundedBox(self._x, self._y, self._width, self._height)
		self._hitbox_offset_x = 0
		self._hitbox_offset_y = 0


	@property
	def hitbox_offset_x(self):
		return self._hitbox_offset_x
	@hitbox_offset_x.setter
	def hitbox_offset_x(self, hitbox_offset_x):
		hitbox_offset_x = int(hitbox_offset_x)
		self._hitbox_offset_x = hitbox_offset_x
		self.x = self.x + hitbox_offset_x

	@property
	def hitbox_offset_y(self):
		return self._hitbox_offset_y
	@hitbox_offset_y.setter
	def hitbox_offset_y(self, hitbox_offset_y):
		hitbox_offset_y = int(hitbox_offset_y)
		self._hitbox_offset_y = hitbox_offset_y
		self.y = self.y + hitbox_offset_y

	def _set_object_x(self, x):
		self.hitbox.x = x
		self._set_sprite_x(self.hitbox.x - self._hitbox_offset_x)

	def _set_object_x2(self, x2):
		self.hitbox.x2 = x2
		self._set_sprite_x(self.hitbox.x - self._hitbox_offset_x)

	def _set_object_x_tile(self, x_tile):
		self.hitbox.x_tile = x_tile
		self._set_sprite_x(self.hitbox.x - self._hitbox_offset_x)

	def _set_object_x2_tile(self, x2_tile):
		self.hitbox.x2_tile = x2_tile
		self._set_sprite_x(self.hitbox.x - self._hitbox_offset_x)

	def _set_object_tile_x(self, tile_x):
		self.hitbox.tile_x = tile_x
		self._set_sprite_x(self.hitbox.x - self._hitbox_offset_x)

	def _set_object_tile_x2(self, tile_x2):
		self.hitbox.tile_x2 = tile_x2
		self._set_sprite_x(self.hitbox.x - self._hitbox_offset_x)

	x = property(lambda self: self.hitbox.x, _set_object_x)
	x2 = property(lambda self: self.hitbox.x2, _set_object_x2)
	x_tile = property(lambda self: self.hitbox.x_tile, _set_object_x_tile)
	x2_tile = property(lambda self: self.hitbox.x2_tile, _set_object_x2_tile)
	tile_x = property(lambda self: self.hitbox.tile_x, _set_object_tile_x)
	tile_x2 = property(lambda self: self.hitbox.tile_x2, _set_object_tile_x2)


	def _set_object_y(self, y):
		self.hitbox.y = y
		self._set_sprite_y(self.hitbox.y - self._hitbox_offset_y)

	def _set_object_y2(self, y2):
		self.hitbox.y2 = y2
		self._set_sprite_y(self.hitbox.y - self._hitbox_offset_y)

	def _set_object_y_tile(self, y_tile):
		self.hitbox.y_tile = y_tile
		self._set_sprite_y(self.hitbox.y - self._hitbox_offset_y)

	def _set_object_y2_tile(self, y2_tile):
		self.hitbox.y2_tile = y2_tile
		self._set_sprite_y(self.hitbox.y - self._hitbox_offset_y)

	def _set_object_tile_y(self, tile_y):
		self.hitbox.tile_y = tile_y
		self._set_sprite_y(self.hitbox.y - self._hitbox_offset_y)

	def _set_object_tile_y2(self, tile_y2):
		self.hitbox.tile_y2 = tile_y2
		self._set_sprite_y(self.hitbox.y - self._hitbox_offset_y)

	y = property(lambda self: self.hitbox.y, _set_object_y)
	y2 = property(lambda self: self.hitbox.y2, _set_object_y2)
	y_tile = property(lambda self: self.hitbox.y_tile, _set_object_y_tile)
	y2_tile = property(lambda self: self.hitbox.y2_tile, _set_object_y2_tile)
	tile_y = property(lambda self: self.hitbox.tile_y, _set_object_tile_y)
	tile_y2 = property(lambda self: self.hitbox.tile_y2, _set_object_tile_y2)


	@property
	def width(self):
		return self.hitbox.width
	@property
	def half_width(self):
		return self.hitbox.half_width
	@property
	def tile_width(self):
		return self.hitbox.tile_width
	@property
	def half_tile_width(self):
		return self.hitbox.half_tile_width
	@property
	def tile_width_span(self):
		return self.hitbox.tile_width_span


	@property
	def height(self):
		return self.hitbox.height
	@property
	def half_height(self):
		return self.hitbox.half_height
	@property
	def tile_height(self):
		return self.hitbox.tile_height
	@property
	def half_tile_height(self):
		return self.hitbox.half_tile_height
	@property
	def tile_height_span(self):
		return self.hitbox.tile_height_span
