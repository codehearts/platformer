from pyglet.gl import *
from ..settings.general_settings import TILE_SIZE
from ..bounded_box import BoundedBox
from viewport import Viewport
from ..easing import EaseOut

# TODO on_target_change event

# TODO Specify the type of `target` in the docstring
class Camera(Viewport):
	"""A camera which can be used to follow specific objects.

	Attributes:
		target (TODO): The object being followed by the camera.
	"""

	def __init__(self, *args, **kwargs):
		"""Creates a new camera.

		Kwargs:
			bounds (BoundedBox): Limit the position of the viewport to within these bounds.
			target (:class:`game.physical_objects.PhysicalObject`): A physical object to have the camera follow.
			ease_timing (float): A time duration, in seconds, which determines how quickly the camera follows the target.
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis. Optional.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis. Optional.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis. Optional.
		"""
		self.target = kwargs.pop('target', None)
		self.ease_timing = kwargs.pop('ease_timing', 0.25)

		easing = kwargs.pop('easing', None)
		x_easing = kwargs.pop('y_easing', None)
		y_easing = kwargs.pop('x_easing', None)

		super(Camera, self).__init__(*args, **kwargs)

		# Use ease out as the default easing function
		self._default_easing_function = EaseOut
		self._x_easing_function, self._y_easing_function = self._get_easing_functions(easing, x_easing, y_easing)

		# Immediately focus on the target
		self._easing_x = self._x_easing_function(self.target.mid_x, self.target.mid_x, self.ease_timing)
		self._easing_y = self._y_easing_function(self.target.mid_y, self.target.mid_y, self.ease_timing)

		# True if the camera is following the target
		self._focusing_on_target = True

		# True if the camera is returning to the target's coordinates
		self._returning_to_target = False

		# Needed for adjusting the viewport with OpenGL

		self._aspect = self.width / float(self.height)
		self._scale = self.height / 2

		self._left   = -self._scale * self._aspect
		self._right  =  self._scale * self._aspect
		self._bottom = -self._scale
		self._top    =  self._scale

		# Focus the camera on the target
		self.update(0)

	# @TODO Camera should focus a few tiles ahead of the direction the target is facing

	def update(self, dt):
		"""Updates the position of the camera based on where its supposed to be focusing.

		Args:
			dt (float): The number of seconds between the current frame and the previous frame.
		"""
		self._easing_x.update(dt)
		self._easing_y.update(dt)

		if self._focusing_on_target:
			# If the camera is focusing on the target, adjust its destination to the target's coordinates
			if self.target.mid_x != self._easing_x.end:
				self._easing_x.change_end(self.target.mid_x)
			if self.target.mid_y != self._easing_y.end:
				self._easing_y.change_end(self.target.mid_y)
		elif self._easing_x.is_done() and self._easing_y.is_done() and self._returning_to_target:
			# If the camera is done returning to the target's coordinates, begin following the target
			self._focusing_on_target = True
			self._returning_to_target = False
			self._easing_x = self._x_easing_function(self._easing_x.value, self.target.mid_x, self.ease_timing)
			self._easing_y = self._y_easing_function(self._easing_y.value, self.target.mid_y, self.ease_timing)

		super(Camera, self).update(0, self._easing_x.value - self.half_width, self._easing_y.value - self.half_height)

	def focus(self):
		"""Focuses the camera, adjusting the viewport to be where it should be for the next frame."""
		# Get the coordinates as integers to prevent rendering issues
		x = self.mid_x
		y = self.mid_y

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self._left, self._right, self._bottom, self._top)
		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def focus_on_coordinates(self, x, y, duration=1, easing=None, x_easing=None, y_easing=None):
		"""Focuses the camera on the given coordinates.

		Args:
			x (int): The x coordinate.
			y (int): The y coordinate.

		Kwargs:
			duration (float): The amount of time, in seconds, that the camera should take to focus on the coordinates.
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis. Optional.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis. Optional.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis. Optional.
		"""
		self._focusing_on_target = False
		x_easing, y_easing = self._get_easing_functions(easing, x_easing, y_easing)

		coordinates = BoundedBox(x - self._half_width, y - self._half_height, 0, 0).bound_within(self.bounds)

		self._easing_x = x_easing(self._easing_x.value, coordinates.x, duration)
		self._easing_y = y_easing(self._easing_y.value, coordinates.y, duration)

	def focus_on_tile(self, tile_x, tile_y, *args, **kwargs):
		"""Focuses the camera on the given tile.

		Args:
			tile_x (int): The tile's x position.
			tile_y (int): The tile's y position.

		Kwargs:
			duration (float): The amount of time, in seconds, that the camera should take to focus on the tile.
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis. Optional.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis. Optional.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis. Optional.
		"""
		self.focus_on_coordinates(tile_x * TILE_SIZE, tile_y * TILE_SIZE, *args, **kwargs)

	def focus_on_target(self, *args, **kwargs):
		"""Focuses the camera back on the target.

		Kwargs:
			duration (float): The amount of time, in seconds, that the camera should take to focus on the target.
			easing (:class:`easing.Linear`): An easing function to use for the x and y axis. Optional.
			x_easing (:class:`easing.Linear`): An easing function to use for the x axis. Optional.
			y_easing (:class:`easing.Linear`): An easing function to use for the y axis. Optional.
		"""
		# Flag that the camera is returning to the target's coordinates
		self._returning_to_target = True

		self.focus_on_coordinates(self.target.mid_x + self._half_width, self.target.mid_y + self._half_height, *args, **kwargs)

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
