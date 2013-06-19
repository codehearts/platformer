from game.bounded_box import BoundedBox

class Viewport(BoundedBox):
	"""An abstract representation of a viewport.

	This class is primarily intended for use in testing.
	:class:`game.viewport.Camera` is more useful for in-game.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Kwargs:
			bounds (BoundedBox): Limit the position of the viewport to within these bounds.
		"""
		self.bounds = kwargs.pop('bounds', None)

		super(Viewport, self).__init__(*args, **kwargs)

		# If we have boundaries, the bounding function should bound the viewport within them
		# Otherwise, we don't need a bounding function
		if self.bounds:
			self._bound_viewport = lambda: self.bound_within(self.bounds)
		else:
			self._bound_viewport = lambda: None



	def update(self, dt, x, y):
		"""Updates the position of the viewport.

		Args:
			dt (float): The number of seconds between the current frame and the previous frame.
			x (int): The x coordinate to move the viewport to.
			y (int): The y coordinate to move the viewport to.
		"""
		self._set_x(x)
		self._set_y(y)

		self._bound_viewport()
