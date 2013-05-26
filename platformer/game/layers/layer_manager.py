import pyglet

# TODO Write tests for this
class LayerManager(object):

	# TODO Document the list syntax
	def __init__(self, bg_layers, fg_layers):
		self.bg_batch = pyglet.graphics.Batch()
		self.fg_batch = pyglet.graphics.Batch()

		# TODO If a layer is ever deleted, batches should be coerced if possible
		self.bg_drawing_queue = []
		self.fg_drawing_queue = []
		self.layers = []

		# Add all background layers to the background batch
		#map(lambda bg_layer: bg_layer.set_batch(self.bg_batch), bg_layers)
		# TODO This code shouldn't be dulicated
		for bg_layer in bg_layers:
			# If this layer supports batches, add it to the current batch in the drawing queue
			if bg_layer.supports_batches():
				# If the current item in the drawing queue is not a batch, create a batch and add it
				if not self.bg_drawing_queue or not isinstance(self.bg_drawing_queue[-1], pyglet.graphics.Batch):
					self.bg_drawing_queue.append(pyglet.graphics.Batch())

				bg_layer.set_batch(self.bg_drawing_queue[-1])
			# If the layer doesn't support batches, it will be asked to draw itself
			else:
				self.bg_drawing_queue.append(bg_layer)

			self.layers.append(bg_layer)

		# Add all foreground layers to the foreground batch
		#map(lambda fg_layer: fg_layer.layer.set_batch(self.fg_batch), fg_layers)
		for fg_layer in fg_layers:
			# If this layer supports batches, add it to the current batch in the drawing queue
			if fg_layer.supports_batches():
				# If the current item in the drawing queue is not a batch, create a batch and add it
				if not self.fg_drawing_queue or not isinstance(self.fg_drawing_queue[-1], pyglet.graphics.Batch):
					self.fg_drawing_queue.append(pyglet.graphics.Batch())

				fg_layer.set_batch(self.fg_drawing_queue[-1])
			# If the layer doesn't support batches, it will be asked to draw itself
			else:
				self.fg_drawing_queue.append(fg_layer)

			self.layers.append(fg_layer)

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
		map(lambda layer: layer.draw(), self.bg_drawing_queue)

	# Draw the foreground to the screen
	def draw_foreground(self):
		map(lambda layer: layer.draw(), self.fg_drawing_queue)
