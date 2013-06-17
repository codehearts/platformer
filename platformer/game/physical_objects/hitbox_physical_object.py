from physical_object import PhysicalObject
from game.bounded_box import BoundedBox

# TODO Could draw hitbox overlays using pyglet.image.SolidColorImagePattern
# TODO Create a MultiHitboxPhysicalObject class

class HitboxPhysicalObject(PhysicalObject):

	def __init__(self, *args, **kwargs):
		# Temporary hitbox for during initialization
		self.hitbox = BoundedBox(0, 0, 0, 0)

		self._hitbox_offset_x = 0
		self._hitbox_offset_y = 0

		super(HitboxPhysicalObject, self).__init__(*args, **kwargs)

		# Create our actual hitbox from the physical object's dimensions
		self.hitbox = BoundedBox(self._x, self._y, self._width, self._height)



	# TODO Test this class's hitbox coordinates
	def _get_hitbox_offset_x(self, hitbox_offset_x):
		hitbox_offset_x = int(hitbox_offset_x)
		self._hitbox_offset_x = hitbox_offset_x
		self.x = self.x + hitbox_offset_x

	hitbox_offset_x = property(lambda self: self._hitbox_offset_x, _get_hitbox_offset_x)


	def _get_hitbox_offset_y(self, hitbox_offset_y):
		hitbox_offset_y = int(hitbox_offset_y)
		self._hitbox_offset_y = hitbox_offset_y
		self.y = self.y + hitbox_offset_y

	hitbox_offset_y = property(lambda self: self._hitbox_offset_y, _get_hitbox_offset_y)



	def _set_x(self, x):
		self.hitbox.x = x
		PhysicalObject._set_x(self, self.hitbox.x - self._hitbox_offset_x)

	x = property(lambda self: self.hitbox.x, _set_x)


	def _set_mid_x(self, mid_x):
		self.hitbox.mid_x = mid_x
		PhysicalObject._set_x(self, self.hitbox.x - self._hitbox_offset_x)

	mid_x = property(lambda self: self.hitbox.mid_x, _set_mid_x)


	def _set_x2(self, x2):
		self.hitbox.x2 = x2
		PhysicalObject._set_x(self, self.hitbox.x - self._hitbox_offset_x)

	x2 = property(lambda self: self.hitbox.x2, _set_x2)


	def _set_x_tile(self, x_tile):
		self.hitbox.x_tile = x_tile
		PhysicalObject._set_x(self, self.hitbox.x - self._hitbox_offset_x)

	x_tile = property(lambda self: self.hitbox.x_tile, _set_x_tile)


	def _set_mid_x_tile(self, mid_x_tile):
		self.hitbox.mid_x_tile = mid_x_tile
		PhysicalObject._set_x(self, self.hitbox.x - self._hitbox_offset_x)

	mid_x_tile = property(lambda self: self.hitbox.mid_x_tile, _set_mid_x_tile)


	def _set_x2_tile(self, x2_tile):
		self.hitbox.x2_tile = x2_tile
		PhysicalObject._set_x(self, self.hitbox.x - self._hitbox_offset_x)

	x2_tile = property(lambda self: self.hitbox.x2_tile, _set_x2_tile)



	def _set_y(self, y):
		self.hitbox.y = y
		PhysicalObject._set_y(self, self.hitbox.y - self._hitbox_offset_y)

	y = property(lambda self: self.hitbox.y, _set_y)


	def _set_mid_y(self, mid_y):
		self.hitbox.mid_y = mid_y
		PhysicalObject._set_y(self, self.hitbox.y - self._hitbox_offset_y)

	mid_y = property(lambda self: self.hitbox.mid_y, _set_mid_y)


	def _set_y2(self, y2):
		self.hitbox.y2 = y2
		PhysicalObject._set_y(self, self.hitbox.y - self._hitbox_offset_y)

	y2 = property(lambda self: self.hitbox.y2, _set_y2)


	def _set_y_tile(self, y_tile):
		self.hitbox.y_tile = y_tile
		PhysicalObject._set_y(self, self.hitbox.y - self._hitbox_offset_y)

	y_tile = property(lambda self: self.hitbox.y_tile, _set_y_tile)


	def _set_mid_y_tile(self, mid_y_tile):
		self.hitbox.mid_y_tile = mid_y_tile
		PhysicalObject._set_y(self, self.hitbox.y - self._hitbox_offset_y)

	mid_y_tile = property(lambda self: self.hitbox.mid_y_tile, _set_mid_y_tile)


	def _set_y2_tile(self, y2_tile):
		self.hitbox.y2_tile = y2_tile
		PhysicalObject._set_y(self, self.hitbox.y - self._hitbox_offset_y)

	y2_tile = property(lambda self: self.hitbox.y2_tile, _set_y2_tile)



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
