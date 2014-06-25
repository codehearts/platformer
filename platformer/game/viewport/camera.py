from pyglet.gl import *
from ..settings.general_settings import TILE_SIZE
from viewport import Viewport
from ..easing import EaseOut
from game.graphics import install_graphics_module

# TODO on_target_change event

# TODO Specify the type of `target` in the docstring
class Camera(Viewport):
	"""A camera which can be used to follow specific objects.

	Attributes:
		target (): The object being followed by the camera.
	"""

	def __init__(self, *args, **kwargs):
		"""Creates a new camera.

		Kwargs:
			target (:class:`game.physical_objects.PhysicalObject`): A physical object to have the camera follow.
		"""
		self.target = kwargs.pop('target', None)
		self.ease_timing = kwargs.pop('ease_timing', 0.4)

		super(Camera, self).__init__(*args, **kwargs)

		# Accuracy threshold for focusing on targets
		self.accuracy_threshold = 2

		self.easing_x = EaseOut(self.target.mid_x, self.target.mid_x, self.ease_timing)
		self.easing_y = EaseOut(self.target.mid_y, self.target.mid_y, self.ease_timing)

		self.seeking_target = False
		self.go_for_target = False

		self.aspect = self.width / float(self.height)
		self.scale = self.height / 2

		self.left   = -(self.scale) * self.aspect
		self.right  = self.scale * self.aspect
		self.bottom = -(self.scale)
		self.top    = self.scale

	# @TODO Camera should slowly follow player
	# @TODO Camera should focus a few tiels ahead of the direction the target is facing

	def update(self, dt):
		self.easing_x.update(dt)
		self.easing_y.update(dt)

		if self.seeking_target:
			if self.target.mid_x != self.easing_x.end:
				self.easing_x.change_end(self.target.mid_x)

			if self.target.mid_y != self.easing_y.end:
				self.easing_y.change_end(self.target.mid_y)
		elif self.easing_x.is_done() and self.easing_y.is_done() and self.go_for_target:
			self.seeking_target = True
			self.go_for_target = False
			self.easing_x = EaseOut(self.easing_x.value, self.target.mid_x, self.ease_timing)
			self.easing_y = EaseOut(self.easing_y.value, self.target.mid_y, self.ease_timing)

		x = self.easing_x.value - self.half_width
		y = self.easing_y.value - self.half_height

		super(Camera, self).update(0, x, y)

	def draw(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self.left, self.right, self.bottom, self.top)
		x = int(self.easing_x.value)
		y = int(self.easing_y.value)
		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def focus_on_target(self, duration=1, easing=None, x_easing=None, y_easing=None):
		print("TARGET FOCUS")
		self.go_for_target = True

		# Initialize the easing function
		if not easing is None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing is None:
				x_easing = EaseOut
			if y_easing is None:
				y_easing = EaseOut

		self.easing_x = x_easing(self.easing_x.value, self.target.mid_x, duration)
		self.easing_y = y_easing(self.easing_y.value, self.target.mid_y, duration)

	def move_to(self, x, y, duration=1, easing=None, x_easing=None, y_easing=None):
		print("MOVE TO")

		# Initialize the easing function
		if not easing is None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing is None:
				x_easing = EaseOut
			if y_easing is None:
				y_easing = EaseOut

		self.easing_x = x_easing(self.easing_x.value, x - self._half_width, duration)
		self.easing_y = y_easing(self.easing_y.value, y - self._half_height, duration)

	def move_to_tile(self, tile_x, tile_y, *args, **kwargs):
		self.move_to(tile_x * TILE_SIZE, tile_y * TILE_SIZE, *args, **kwargs)


def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.tiles.tileset.Tileset`."""
	return graphics_type == 'camera'

def factory(*args, **kwargs):
	"""Returns a :class:`game.tiles.tileset.Tileset` for the given arguments."""
	return Camera(*args, **kwargs)

install_graphics_module(__name__)
