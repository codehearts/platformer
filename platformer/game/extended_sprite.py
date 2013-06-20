from bounded_box import BoundedBox
from pyglet.sprite import Sprite

class ExtendedSprite(BoundedBox, Sprite):
	""":class:`pgylet.sprite.Sprite` which tracks its position and dimensions in terms of pixels and tiles."""

	def __init__(self, *args, **kwargs):
		Sprite.__init__(self, *args, **kwargs)

		self._width = self._texture.width * self._scale
		self._height = self._texture.height * self._scale
		BoundedBox.__init__(self, self._x, self._y, self._width, self._height)



	def _set_x(self, x):
		BoundedBox._set_x(self, x)
		Sprite._set_x(self, self._x)

	x = property(lambda self: self._x, _set_x)



	def _set_y(self, y):
		BoundedBox._set_y(self, y)
		Sprite._set_y(self, self._y)

	y = property(lambda self: self._y, _set_y)



	# TODO Unit tests
	def set_position(self, x, y):
		"""Set the x and y coordinates of the sprite simultaneously.

		Args:
			x (int): x coordinate of the sprite.
			y (int): y coordinate of the sprite.
        """
		self._set_x(x)
		self._set_y(y)

	position = property(lambda self: (self._x, self._y), set_position)
