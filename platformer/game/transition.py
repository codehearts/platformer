from resources import transition_sprite
from animation import tiled_animation
from text import heading

# TODO This class can probably be deleted
class Transition(object):

	def __init__(self, camera, text='', batch=None):
		self.camera = camera

		self.transition_animation = tiled_animation.TiledAnimation(transition_sprite.sprite, camera.width, camera.height, delay=0.5, duration=1.25, ease_power=1.75)
		self.heading = heading.Heading(text, duration=2.25, batch=batch)

	def update(self, dt):
		self.transition_animation.update(dt)
		# TODO Are focus_x and focus_y necessarily the center? Should these properties be renamed, as the camera focus may not necessarily be centered?
		self.heading.update(dt, x=self.camera.focus_x, y=self.camera.focus_y)

	def draw(self):
		self.transition_animation.draw(self.camera.x, self.camera.y)

	def is_done(self):
		return self.heading.is_done and self.transition_animation.is_done

	def set_batch(self, batch):
		self.heading.set_batch(batch)
