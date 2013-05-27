from pyglet.graphics import Batch

# TODO Write tests for this
class LayerManager(object):
	"""Manager for maintaining and drawing multiple background and foreground layers in a specified order.

	Attributes:
		layers (list): A list of all layers currently being managed.
	"""

	# TODO This could possibly accept a single list, and I could just pass the stage like any other layer
	def __init__(self, bg_layers, fg_layers):
		"""Creates a new manager for the given layers.

		Args:
			bg_layers: A list of the layers to be rendered in the background, with lower indices in the list being drawn further towards the background.
			fg_layers: A list of the layers to be rendered in the foreground, with lower indices in the list being drawn further towards the background.
		"""
		# TODO If a layer is ever deleted, batches should be coerced if possible
		self._bg_drawing_queue = []
		self._fg_drawing_queue = []
		self.layers = []

		# Add all layers to the drawing queue
		map(lambda layer: self.append_to_drawing_queue(layer, self._bg_drawing_queue), bg_layers)
		map(lambda layer: self.append_to_drawing_queue(layer, self._fg_drawing_queue), fg_layers)

		# Keep track of all layers
		self.layers = bg_layers + fg_layers

	def update(self, dt):
		"""Updates all managed layers.

		Args:
			dt: The time delta (in seconds) between the current frame and the previous frame.
		"""
		map(lambda layer: layer.update(dt), self.layers)

	def draw_background(self):
		"""Draws all background layers."""
		map(lambda layer: layer.draw(), self._bg_drawing_queue)

	def draw_foreground(self):
		"""Draws all foreground layers."""
		map(lambda layer: layer.draw(), self._fg_drawing_queue)

	def append_to_drawing_queue(self, layer, queue):
		"""Adds the layer to the drawing queue.

		If the layer supports batches, it will be added to a batch
		at the end of the queue. If the layer does not support batches,
		the layer itself will be added to the end of the queue.

		Args:
			layer: The layer to append to the queue.
			queue: The queue to append the layer to.
		"""
		# If this layer supports batches, add it to the current batch in the drawing queue
		if layer.supports_batches():
			# If the current item in the drawing queue is not a batch, create a batch and add it to the queue
			if not queue or not isinstance(queue[-1], Batch):
				queue.append(Batch())

			layer.set_batch(queue[-1])
		# If this layer doesn't support batches, it will be asked to draw itself
		else:
			queue.append(layer)
