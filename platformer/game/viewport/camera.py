from pyglet.gl import *
from ..settings.general_settings import TILE_SIZE
from viewport import Viewport
from ..easing import EaseIn, EaseOut

# TODO on_target_change event

# TODO Specify the type of `target` in the docstring
class Camera(Viewport):
	"""A camera which can be used to follow specific objects.

	Attributes:
		target (): The object being followed by the camera.
	"""

	# TODO Does the target need to be a PhysicalObject or can it be a BoundedBox?
	def __init__(self, *args, **kwargs):
		"""Creates a new camera.

		Kwargs:
			target (:class:`game.physical_objects.PhysicalObject`): A physical object to have the camera follow.
		"""
		self.target = kwargs.pop('target', None)

		super(Camera, self).__init__(*args, **kwargs)

		self.easing_x = None
		self.easing_y = None

		# Accuracy threshold for focusing on targets
		self.accuracy_threshold = 2

		self.focus_x = 0
		self.focus_y = 0

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
		if self.easing_x or self.easing_y:
			if self.easing_x:
				self.easing_x.update(dt)
				self.focus_x = int(self.easing_x.value)
			if self.easing_y:
				self.easing_y.update(dt)
				self.focus_y = int(self.easing_y.value)

			self.focus_on(self.focus_x, self.focus_y)

			if self.easing_x.value == self.easing_x.end:
				self.easing_x = None
			if self.easing_y.value == self.easing_y.end:
				self.easing_y = None

			if not self.easing_x and not self.easing_y:
				if self.seeking_target:
					self.seeking_target = False
				else:
					self.fixed = True
		elif not self.fixed:
			self.focus()



	def focus(self):
		x = self.target.mid_x
		y = self.target.mid_y

		# Keep the camera within the bounds of the stage
		super(Camera, self).update(0, x - self._half_width, y - self._half_height)

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
		# Initialize the easing function
		if easing != None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing == None:
				x_easing = EaseIn
			if y_easing == None:
				y_easing = EaseIn

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
		# Initialize the easing function
		if easing != None:
			x_easing = easing
			y_easing = easing
		else:
			if x_easing == None:
				x_easing = EaseIn
			if y_easing == None:
				y_easing = EaseIn

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
