import pyglet

class LayerManager(object):

	# TODO Document the list syntax
	def __init__(self, bg_layers, fg_layers):
		self.bg_batch = pyglet.graphics.Batch()
		self.fg_batch = pyglet.graphics.Batch()
		self.batched_bg_layers = []
		self.unbatched_bg_layers = []
		self.batched_fg_layers = []
		self.unbatched_fg_layers = []
		self.layers = []

		# Add all background layers to the background batch
		#map(lambda bg_layer: bg_layer['layer'].set_batch(self.bg_batch), bg_layers)
		# TODO This code shouldn't be dulicated
		for bg_layer in bg_layers:
			if not 'use_batch' in bg_layer or bg_layer['use_batch']:
				bg_layer['layer'].set_batch(self.bg_batch)
				self.batched_bg_layers.append(bg_layer['layer'])
			else:
				self.unbatched_bg_layers.append(bg_layer['layer'])

			self.layers.append(bg_layer['layer'])

		# Add all foreground layers to the foreground batch
		#map(lambda fg_layer: fg_layer.layer.set_batch(self.fg_batch), fg_layers)
		for fg_layer in fg_layers:
			if not 'use_batch' in fg_layer or fg_layer['use_batch']:
				fg_layer['layer'].set_batch(self.fg_batch)
				self.batched_fg_layers.append(fg_layer['layer'])
			else:
				self.unbatched_fg_layers.append(fg_layer['layer'])

			self.layers.append(fg_layer['layer'])

		# @TODO 2 or 3 layers of parallax backgrounds
		# @TODO Non-collidable background midground layer

		# @TODO Is this necessary?
		self.update(0)

	def update(self, dt):
		map(lambda layer: layer.update(dt), self.layers)
		"""
		self.bg.update(dt)
		self.overlay.update(dt)
		"""

	# Draw the background to the screen
	def draw_background(self):
		self.bg_batch.draw()

	# Draw the foreground to the screen
	def draw_foreground(self):
		self.fg_batch.draw()
		map(lambda layer: layer.draw(), self.unbatched_fg_layers)
