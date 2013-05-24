import pyglet
from game import overlay

# TODO This should be made into a general purpose Layer object (or something) which has a subclass for fixed and parallax and whatnot layers
class Background(object):

	# TODO I feel like the ideal thing would be for the background to not be aware of the viewport
	def __init__(self, image, viewport, batch=None):
		self.viewport = viewport
		self.image = pyglet.sprite.Sprite(img=image, x=viewport.x, y=viewport.y, batch=batch)

	def update(self, dt):
		self.image.x = self.viewport.x
		self.image.y = self.viewport.y

# TODO Move this class to its own file
class Layers(object):

	# TODO This should accept a list of background objects and a list of foreground objects and handle their rendering and updating
	# The viewport defines what each layer should be relative to, and should have an x and y property
	def __init__(self, tile_data, viewport):
		self.bg_batch = pyglet.graphics.Batch()
		self.fg_batch = pyglet.graphics.Batch()
		self.viewport = viewport

		# TODO This object should be made outside this class and passed in
		self.bg = Background(pyglet.resource.image(tile_data.get_background_image_file()), viewport, batch=self.bg_batch)

		# TODO The overlay should not be bound to the background, there should be a layering class or something which handles these
		self.overlay = overlay.Overlay(tile_data, self.fg_batch, self.viewport)

		# @TODO 2 or 3 layers of parallax backgrounds
		# @TODO Non-collidable background midground layer

		# @TODO Is this necessary?
		self.update(0)

	def update(self, dt):
		self.bg.update(dt)
		self.overlay.update(dt)

	# Draw the background to the screen
	def draw_background(self):
		self.bg_batch.draw()

	# Draw the foreground to the screen
	def draw_foreground(self):
		self.fg_batch.draw()
		self.overlay.draw()
