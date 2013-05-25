import pyglet, math, transition
from settings import general_settings

class Overlay(object):

	# TODO title could be called "heading" or something better
	def __init__(self, title, viewport, batch=None):
		self.show_fps = True

		self.viewport = viewport

		# TODO This equation should be kept in a function
		self.tile_width = int(math.ceil(viewport.width / general_settings.TILE_SIZE_FLOAT))
		self.tile_height = int(math.ceil(viewport.height / general_settings.TILE_SIZE_FLOAT))

		# TODO The Transition class should really be repurposed and organized
		self.transition = transition.Transition(viewport, title)

		if self.show_fps:
			self.fps_text = pyglet.text.Label(str(pyglet.clock.get_fps()), font_name='Helvetica Neue', font_size=18, x=viewport.x+10, y=viewport.y2-10, batch=batch)

	def update(self, dt):
		if self.show_fps:
			self.fps_text.text = str(int(pyglet.clock.get_fps()))
			self.fps_text.x = self.viewport.x + 10
			self.fps_text.y = self.viewport.y + 10

		if self.transition:
			self.transition.update(dt)

	def draw(self):
		if self.transition:
			self.transition.draw()

			if self.transition.is_done:
				self.transition = None

	def set_batch(self, new_batch):
		# Asign a new batch for the fps text if it exists
		if self.fps_text:
			self.fps_text.batch = new_batch
