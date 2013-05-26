import pyglet, math, transition
from settings import general_settings

# TODO This class is less of an overlay and more of a transition class with FPS support
class Overlay(object):

	# TODO title could be called "heading" or something better
	def __init__(self, title, viewport, batch=None):
		# TODO The FPS should not be tethered to this class
		# TODO This should be some sort of setting somewhere
		self.show_fps = True

		self.viewport = viewport

		# TODO This equation should be kept in a function
		self.tile_width = int(math.ceil(viewport.width / general_settings.TILE_SIZE_FLOAT))
		self.tile_height = int(math.ceil(viewport.height / general_settings.TILE_SIZE_FLOAT))

		# TODO The Transition class should really be repurposed and organized
		self.transition = transition.Transition(viewport, title, batch=batch)

		if self.show_fps:
			# TODO This font should be changed, preferably to something that can be placed in the resources folder
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

			if self.transition.is_done():
				self.transition = None

	def set_batch(self, new_batch):
		self.transition.set_batch(new_batch)

		# Asign a new batch for the fps text if it exists
		if self.fps_text:
			self.fps_text.begin_update()
			self.fps_text.batch = new_batch
			self.fps_text.end_update()
