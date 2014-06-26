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

		self._x_easing_function, self._y_easing_function = self._get_easing_functions(easing, x_easing, y_easing)

		# Immediately focus on the target
		self._easing_x = self._x_easing_function(self.target.mid_x, self.target.mid_x, self.ease_timing)
		self._easing_y = self._y_easing_function(self.target.mid_y, self.target.mid_y, self.ease_timing)

		# True if the camera is following the target
		self._focusing_on_target = True
		self.fixed = False

		# True if the camera is returning to the target's coordinates
		self._returning_to_target = False

		# Focus the camera on the target
		self.update(0)

	# @TODO Camera should focus a few tiles ahead of the direction the target is facing

	def update(self, dt):
		"""Updates the position of the camera based on where its supposed to be focusing.

		Args:
			dt (float): The number of seconds between the current frame and the previous frame.
		"""
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

		super(Camera, self).update(dt)

	def focus_on_coordinates(self, *args, **kwargs):
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
		self._focusing_on_target = False
		super(Camera, self).focus_on_coordinates(*args, **kwargs)

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

		self.focus_on_coordinates(self.target.mid_x, self.target.mid_y, *args, **kwargs)
