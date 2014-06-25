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

		super(Camera, self).__init__(*args, **kwargs)

		# Accuracy threshold for focusing on targets
		self.accuracy_threshold = 2

		self.focus_x = self.target.mid_x
		self.focus_y = self.target.mid_y

		self.time = 0.4
		self.easing_x = EaseOut(self.focus_x, self.focus_x, self.time)
		self.easing_y = EaseOut(self.focus_y, self.focus_y, self.time)

		self.seeking_target = False
		self.fixed = False

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

		x = self.easing_x.value - self.half_width
		y = self.easing_y.value - self.half_height

		super(Camera, self).update(0, x, y)

		self.focus_x = self.target.mid_x
		self.focus_y = self.target.mid_y

		if self.focus_x != self.easing_x.end:
			self.easing_x.change_end(self.focus_x)

		if self.focus_y != self.easing_y.end:
			self.easing_y.change_end(self.focus_y)

	def draw(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self.left, self.right, self.bottom, self.top)
		x = int(self.easing_x.value)
		y = int(self.easing_y.value)
		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()



	def focus(self, easing=None, x_easing=None, y_easing=None):
		print("FOCUS")
		return
		time = 0.4
		# Initialize the easing function
		if not easing is None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing is None:
				x_easing = EaseOut(self.focus_x, 0, time)
			if y_easing is None:
				y_easing = EaseOut(self.focus_x, 0, time)

		self.easing_x = x_easing
		self.easing_y = y_easing

		x = self.target.mid_x
		y = self.target.mid_y

		self.easing_x.change_end(x - self._half_width)
		#self.easing_x.reset_duration(time)
		self.easing_y.change_end(y - self._half_height)
		#self.easing_y.reset_duration(time)

		# Keep the camera within the bounds of the stage
		super(Camera, self).update(0, self.easing_x.value, self.easing_y.value)

		#x -= self._half_width
		#y -= self._half_height

		if x < self.bounds.x + self._half_width:
			x = self._x + self._half_width
		elif x > self.bounds.x2 - self._half_width:
			x = self._x2 - self._half_width

		if y < self._y + self._half_height:
			y = self._y + self._half_height

		self.focus_x = x
		self.focus_y = y

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self.left, self.right, self.bottom, self.top)
		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self._set_x(x - self._half_width)
		self._set_y(y - self._half_height)



	def focus_on(self, x, y):
		print("FOCUS ON")
		super(Camera, self).update(0, x - self._half_width, y - self._half_height)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self.left, self.right, self.bottom, self.top)
		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		if self.seeking_target:
			# Update our target location in case it moved
			self.focus_on_target()

	def focus_on_target(self, time=0.4, easing=None, x_easing=None, y_easing=None):
		print("TARGET FOCUS")
		# Initialize the easing function
		if easing != None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing == None:
				x_easing = EaseOut
			if y_easing == None:
				y_easing = EaseOut

		x = self.target.mid_x
		y = self.target.mid_y

		# If we're already trying to focus on the target, just update our takeoff coordinates and desitination
		if self.seeking_target:
			if x < self._x + self._half_width:
				x = self._x + self._half_width
			elif x > self._x2 - self._half_width:
				x = self._x2 - self._half_width

			if y < self._y + self._half_height:
				y = self._y + self._half_height

			#self.easing_x = x_easing(self.focus_x, x, time)
			#self.easing_y = y_easing(self.focus_y, y, time)
			self.easing_x.change_end(x)
			self.easing_x.reset_duration(time)
			self.easing_y.change_end(y)
			self.easing_y.reset_duration(time)

			# Don't execute the rest of this function if we're already seeking the target
			return

		self.seeking_target = True
		self.fixed = False
		self.move_to(x, y, time, x_easing=x_easing, y_easing=y_easing)



	def move_to(self, x, y, time=1, easing=None, x_easing=None, y_easing=None):
		print("MOVE TO")
		# Initialize the easing function
		if easing != None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing == None:
				x_easing = EaseOut
			if y_easing == None:
				y_easing = EaseOut

		# Keep the camera within the bounds of the stage

		if x < self._x + self._half_width:
			x = self._x + self._half_width
		elif x > self._x2 - self._half_width:
			x = self._x2 - self._half_width

		if y < self._y + self._half_height:
			y = self._y + self._half_height

		self.easing_x = x_easing(self.focus_x, x - self._half_width, time)
		self.easing_y = y_easing(self.focus_y, y - self._half_height, time)

	def move_to_tile(self, tile_x, tile_y, *args, **kwargs):
		self.move_to(tile_x*TILE_SIZE, tile_y*TILE_SIZE, *args, **kwargs)


def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.tiles.tileset.Tileset`."""
	return graphics_type == 'camera'

def factory(*args, **kwargs):
	"""Returns a :class:`game.tiles.tileset.Tileset` for the given arguments."""
	return Camera(*args, **kwargs)

install_graphics_module(__name__)
