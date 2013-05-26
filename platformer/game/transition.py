import pyglet, easing
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from resources import transition_sprite

class Transition(object):

	def __init__(self, camera, heading='', batch=None):
		self.camera = camera

		self.transition_animation = TiledAnimation(transition_sprite.sprite, camera.width, camera.height, delay=0.5, duration=1.25, ease_power=1.75)
		self.heading = Heading(heading, duration=2.25, batch=batch)

	def update(self, dt):
		self.transition_animation.update(dt)
		# TODO Are focus_x and focus_y necessarily the center? Should these properties be renamed, as the camera focus may not necessarily be centered?
		self.heading.update(dt, x=self.camera.focus_x, y=self.camera.focus_y)

	def draw(self):
		self.transition_animation.draw(self.camera.x, self.camera.y)

	def is_done(self):
		return self.heading.is_done and self.transition_animation.is_done

	def set_batch(self, new_batch):
		self.heading.set_batch(new_batch)

# TODO Move this to its own file
class Heading(object):

	# TODO Support for infinite duration (title screens, etc.)
	def __init__(self, heading='', duration=5, batch=None):
		# TODO There could be a generic Timer/Timing class which handles this sort of timing stuff
		self.is_done = False
		self.duration = duration
		self.elapsed_time = 0

		# TODO There should be a setting for the heading typesetting
		# TODO This font should be changed, preferably to something that can be placed in the resources folder
		# TODO Should I be using an HTMLLabel here?
		self.heading = pyglet.text.Label(heading, font_name='Helvetica Neue', font_size=18, anchor_x='center', anchor_y='center', batch=None)

	# TODO When this class is done, this method keeps doing extra work! The parent should be notified to ditch its reference to this object
	def update(self, dt, x=0, y=0):
		self.elapsed_time += dt

		if self.elapsed_time > self.duration:
			self.is_done = True
			self.heading.delete() # Remove this label from its batch
			# TODO Free up the memory this object was using

		self.heading.x = x
		self.heading.y = y

	def set_batch(self, new_batch):
		self.heading.begin_update()
		self.heading.batch = new_batch
		self.heading.end_update()

# TODO Move this to its own file
class TiledAnimation(object):

	# delay - amount of time to wait on the first frame before animating
	# TODO duration should support (and default to) infinite duration (and also support looping)
	def __init__(self, sprite, width, height, delay=0, duration=None, ease_power=2):
		self.sprite = sprite
		self.width = width
		self.height = height

		self.is_done = False

		self.frame_count = len(sprite)
		self.current_frame = 0
		self.delay = delay
		self.duration = duration
		self.elapsed_time = 0
		self.ease_power = ease_power

	def update(self, dt):
		self.elapsed_time += dt

	# TODO Setting coordinates and dimensions here is inconsistent with other classes that accept these parameters on update but not draw, however, it makes sense to pass them here because then the data does not have to be saved in memory until drawing. What should I do?
	def draw(self, x=0, y=0, z=1):
		if self.current_frame < self.frame_count:
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

			self.sprite[self.current_frame].blit_tiled(x, y, z, self.width, self.height)

			# Update the frame on an easing function if we're past the first frame
			if self.elapsed_time > self.delay:
				self.advance_frame()
		else:
			self.is_done = True
			# TODO When done, this object should clear out its space in memory

	def advance_frame(self):
		self.current_frame = int(easing.ease_out(1, self.frame_count, self.duration, self.elapsed_time-self.delay, self.ease_power))
