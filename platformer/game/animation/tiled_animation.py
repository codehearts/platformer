from .. import easing
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

# TODO Support for batches and groups
class TiledAnimation(object):

	# delay - amount of time to wait on the first frame before animating
	# TODO duration should support (and default to) infinite duration (and also support looping)
	# TODO Could this Texture object actually be made into a SpriteGroup with support for batches and groups?
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

	# TODO This class should accept an easing type as a parameter
	def advance_frame(self):
		self.current_frame = int(easing.ease_out(1, self.frame_count, self.duration, self.elapsed_time-self.delay, self.ease_power))
