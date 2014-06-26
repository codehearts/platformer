from pyglet.gl import glMatrixMode, glLoadIdentity, gluOrtho2D, gluLookAt, GL_PROJECTION, GL_MODELVIEW
from game.settings.general_settings import TILE_SIZE
from game.bounded_box import BoundedBox
from game.easing import EaseOut

class Viewport(BoundedBox):
	"""An abstract representation of a viewport.

	This class is primarily intended for use in testing.
	:class:`game.viewport.Camera` is more useful for in-game.
	"""

	def __init__(self, *args, **kwargs):
		"""Creates a new viewport.

		Kwargs:
			bounds (BoundedBox): Limit the position of the viewport to within these bounds.
		"""
		self.bounds = kwargs.pop('bounds', None)

		super(Viewport, self).__init__(*args, **kwargs)

		# Use ease out as the default easing function
		self._default_easing_function = EaseOut

		# True if the viewport should not be moving
		self.fixed = True

		# Easing functions for moving the viewport smoothly
		self._easing_x = None
		self._easing_y = None

		# Needed for adjusting the viewport with OpenGL
		self._aspect =  self.width  / float(self.height)
		self._scale  =  self.height / 2
		self._left   = -self._scale * self._aspect
		self._right  =  self._scale * self._aspect
		self._bottom = -self._scale
		self._top    =  self._scale

		# If we have boundaries, the bounding function should bound the viewport within them
		# Otherwise, we don't need a bounding function
		if self.bounds:
			self._bound_viewport = lambda: self.bound_within(self.bounds)
		else:
			self._bound_viewport = lambda: None



	def update(self, dt):
		"""Updates the position of the viewport.

		Args:
			dt (float): The number of seconds between the current frame and the previous frame.
		"""
		if self.fixed:
			return

		self._easing_x.update(dt)
		self._easing_y.update(dt)

		self._set_x(self._easing_x.value - self.half_width)
		self._set_y(self._easing_y.value - self.half_height)

		# Ensure that the viewport is within the bounds
		self._bound_viewport()

	def focus(self):
		"""Focuses the viewport for the next frame.
		This method should be called before drawing and after clearing the window."""
		x = self.mid_x
		y = self.mid_y

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self._left, self._right, self._bottom, self._top)
		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def focus_on_coordinates(self, x, y, duration=1, easing=None, x_easing=None, y_easing=None):
		"""Focuses the center of the viewport on the given coordinates.

		Args:
			x (int): The x coordinate.
			y (int): The y coordinate.

		Kwargs:
			duration (float): The amount of time, in seconds, that the viewport should take to focus on the coordinates.
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis. Optional.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis. Optional.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis. Optional.
		"""
		self.fixed = False

		x_easing, y_easing = self._get_easing_functions(easing, x_easing, y_easing)

		if self.bounds:
			coordinates = BoundedBox(x, y, 0, 0).bound_within(self.bounds)
			x = coordinates.x
			y = coordinates.y
		else:
			x += self.half_width
			y += self.half_height

		self._easing_x = x_easing(self.mid_x, x, duration)
		self._easing_y = y_easing(self.mid_y, y, duration)

	def focus_on_tile(self, tile_x, tile_y, *args, **kwargs):
		"""Focuses the viewport on the given tile.

		Args:
			tile_x (int): The tile's x position.
			tile_y (int): The tile's y position.

		Kwargs:
			duration (float): The amount of time, in seconds, that the viewport should take to focus on the tile.
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis. Optional.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis. Optional.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis. Optional.
		"""
		self.focus_on_coordinates(tile_x * TILE_SIZE, tile_y * TILE_SIZE, *args, **kwargs)

	def _get_easing_functions(self, easing, x_easing, y_easing):
		"""Returns the appropriate x and y axis easing functions based on the arguments.

		Args:
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis.

		Returns:
			The easing functions as a tuple as (x_easing_function, y_easing_function).
		"""
		if not easing is None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing is None:
				x_easing = self._default_easing_function
			if y_easing is None:
				y_easing = self._default_easing_function

		return (x_easing, y_easing)
