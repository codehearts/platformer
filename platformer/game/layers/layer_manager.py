from pyglet.graphics import Batch, OrderedGroup

# TODO Write tests for this
# TODO Aim to be able to draw everything with a single batch (the current bottleneck for this is my Animation objects, which don't support groups or batches)
class LayerManager(object):
	"""Manager for maintaining and drawing multiple layers in a specified order.

	Attributes:
		layers (list): A list of all layers currently being managed, with lower indices being further towards the background.
	"""

	def __init__(self, layers):
		"""Creates a new manager for the given layers.

		Args:
			layers: A list of the layers to maintain, with lower indices being further towards the background.
		"""
		# TODO If a layer is ever deleted, batches should be coerced if possible
		self._drawing_queue = []
		self._depth = 0 # Number of distinct OrderedGroups in the batch
		self.layers = layers

		# Add all layers to the drawing queue
		map(self.append_to_drawing_queue, layers)

	# TODO Should this class really handle updating objects? Well, it should handle updating layers (like fixed layers), so then it kind of makes sense for this class to handle updates
	def update(self, dt):
		"""Updates all managed layers.

		Args:
			dt: The time delta (in seconds) between the current frame and the previous frame.
		"""
		map(lambda layer: layer.update(dt), self.layers)

	def draw(self):
		map(lambda item: item.draw(), self._drawing_queue)

	def append_to_drawing_queue(self, layer):
		"""Adds the layer to the drawing queue.

		If the layer supports batches, it will be added to a batch
		at the end of the queue. If the layer does not support batches,
		the layer itself will be added to the end of the queue.

		Args:
			layer: The layer to append to the queue.
		"""
		# If this layer supports batches, add it to the current batch in the drawing queue
		if layer.supports_batches():
			# If the current item in the drawing queue is not a batch, create a batch and add it to the queue
			if not self._drawing_queue or not isinstance(self._drawing_queue[-1], Batch):
				self._drawing_queue.append(Batch())

			# Order the rendering of this layer to our current depth
			# TODO This assumes anything that supports batches supports groups (which is a sane assumption, but you never know)
			layer.set_group(OrderedGroup(self._depth))
			self._depth += 1 # Render the next layer at the next depth

			layer.set_batch(self._drawing_queue[-1])
		# If this layer doesn't support batches, it will be asked to draw itself
		else:
			self._drawing_queue.append(layer)
