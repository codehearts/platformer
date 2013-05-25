import pyglet

# TODO This should be made into a general purpose Layer object (or something) which has a subclass for fixed and parallax and whatnot layers
class BasicLayer(object):

	# The viewport defines what each layer should be relative to, and should have an x and y property
	def __init__(self, image, viewport, batch=None):
		self.viewport = viewport
		self.image = pyglet.sprite.Sprite(img=image, x=viewport.x, y=viewport.y, batch=batch)

	def update(self, dt):
		pass

	def set_batch(self, new_batch):
		self.image.batch = new_batch
