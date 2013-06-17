import old_easing
from pyglet.gl import *
from settings import general_settings

class Camera(object):

	def __init__(self, target, window, stage):
		self.target = target
		self.window = window

		self.x = 0
		self.y = 0
		self.x2 = window.width
		self.y2 = window.height
		self.width = window.width
		self.height = window.height
		self.half_width = self.width / 2
		self.half_height = self.height / 2

		# Accuracy threshold for focusing on targets
		self.accuracy_threshold = 2

		self.focus_x = 0
		self.focus_y = 0

		self.takeoff_x = None
		self.takeoff_y = None
		self.destination_x = None
		self.destination_y = None

		self.old_easing_function = general_settings.EASE_IN
		self.ease_time = 0
		self.ease_time_progress = 0

		self.seeking_target = False
		self.fixed = False

		self.aspect = self.width / float(self.height)
		self.scale = self.height / 2

		self.left_boundary	 = self.half_width
		self.right_boundary  = len(stage[0]) * general_settings.TILE_SIZE - self.half_width
		self.bottom_boundary = self.half_height
		self.top_boundary	 = len(stage) * general_settings.TILE_SIZE

		self.left	= -(self.scale) * self.aspect
		self.right	= self.scale * self.aspect
		self.bottom = -(self.scale)
		self.top	= self.scale

	# @TODO Camera should slowly follow player
	# @TODO Camera should focus a few tiels ahead of the direction the target is facing

	def update(self, dt):
		if self.destination_x or self.destination_y:
			self.ease_time_progress += dt

			if self.destination_x:
				if self.old_easing_function == general_settings.EASE_IN:
					self.focus_x = int(old_easing.ease_in(self.takeoff_x, self.destination_x, self.ease_time, self.ease_time_progress))
				else:
					self.focus_x = int(old_easing.ease_out(self.takeoff_x, self.destination_x, self.ease_time, self.ease_time_progress))
			if self.destination_y:
				if self.old_easing_function == general_settings.EASE_IN:
					self.focus_y = int(old_easing.ease_in(self.takeoff_y, self.destination_y, self.ease_time, self.ease_time_progress))
				else:
					self.focus_y = int(old_easing.ease_out(self.takeoff_y, self.destination_y, self.ease_time, self.ease_time_progress))

			self.focus_on(self.focus_x, self.focus_y)

			if self.ease_time_progress >= self.ease_time:
				self.ease_time_progress = 0
				self.destination_x = None
				self.destination_y = None

				if self.seeking_target:
					self.seeking_target = False
				else:
					self.fixed = True
		elif not self.fixed:
			self.focus()



	def focus(self):
		x = self.target.mid_x
		y = self.target.mid_y

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self.left, self.right, self.bottom, self.top)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		# Keep the camera within the bounds of the stage

		if x < self.left_boundary:
			x = self.left_boundary
		elif x > self.right_boundary:
			x = self.right_boundary

		if y < self.bottom_boundary:
			y = self.bottom_boundary

		# Update the camera's anchor point
		self.x = x - self.half_width
		self.y = y - self.half_height
		self.x2 = x + self.half_width
		self.y2 = y + self.half_height

		self.focus_x = x
		self.focus_y = y

		# Update the camera's anchor point
		self.x = x - self.half_width
		self.y = y - self.half_height
		self.x2 = x + self.half_width
		self.y2 = y + self.half_height

		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)



	def focus_on(self, x, y):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		gluOrtho2D(self.left, self.right, self.bottom, self.top)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		# Update the camera's anchor point
		self.x = x - self.half_width
		self.y = y - self.half_height
		self.x2 = x + self.half_width
		self.y2 = y + self.half_height

		gluLookAt(x, y, 1.0, x, y, -1.0, 0, 1, 0.0)

		if self.seeking_target:
			# Update our target location in case it moved
			self.focus_on_target()

	def focus_on_target(self, time=0.4, old_easing=general_settings.EASE_IN):
		x = self.target.mid_x
		y = self.target.mid_y

		# If we're already trying to focus on the target, just update our takeoff coordinates and desitination
		if self.seeking_target:
			if x < self.left_boundary:
				x = self.left_boundary
			elif x > self.right_boundary:
				x = self.right_boundary

			if y < self.bottom_boundary:
				y = self.bottom_boundary

			#self.takeoff_x = self.focus_x
			#self.takeoff_y = self.focus_y
			self.destination_x = x
			self.destination_y = y

			# Don't execute the rest of this function if we're already seeking the target
			return

		self.seeking_target = True
		self.fixed = False
		self.move_to(x, y, time, old_easing)



	def move_to(self, x, y, time=1, old_easing=general_settings.EASE_IN):
		self.ease_time = time
		self.old_easing_function = old_easing
		self.ease_time_progress = 0

		# Keep the camera within the bounds of the stage

		if x < self.left_boundary:
			x = self.left_boundary
		elif x > self.right_boundary:
			x = self.right_boundary

		if y < self.bottom_boundary:
			y = self.bottom_boundary

		self.takeoff_x = self.focus_x
		self.takeoff_y = self.focus_y

		self.destination_x = x
		self.destination_y = y

	def move_to_tile(self, tile_x, tile_y, *args):
		self.move_to(tile_x*general_settings.TILE_SIZE, tile_y*general_settings.TILE_SIZE, *args)
