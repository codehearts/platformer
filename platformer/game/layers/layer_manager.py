from pyglet.graphics import Batch, OrderedGroup

# TODO Write tests for this
# TODO When writing tests, test coalescing and freeing of deleted layers, for ALL types of layers
class LayerManager(object):
	"""Manager for updating and drawing multiple layers in a specified order."""

	def __init__(self, layers):
		"""Begins managing the updating and drawing of the given layers.

		Args:
			layers (list of :class:`game.layers.basic_layer.BasicLayer`): The layers to maintain, with the highest index being the top foreground layer and the first index being the bottom background layer.
		"""
		self._drawing_queue = []
		self._update_queue = []
		self._depth = 0 # Used for setting draw order with OrderedGroups

		# Add all given layers to the manager
		map(self.manage_layer, layers)

	def update(self, dt):
		"""Updates all managed layers which support updating.

		Args:
			dt (number): The time delta (in seconds) between the current frame and the previous frame.
		"""
		map(lambda item: item.update(dt), self._update_queue)

	def draw(self):
		"""Draws all managed layers in the specified order."""
		map(lambda item: item.draw(), self._drawing_queue)

	def manage_layer(self, layer):
		"""Begins managing a layer.

		Args:
			layer (:class:`game.layers.basic_layer.BasicLayer`): The layer to add to the manager.
		"""
		self._append_to_drawing_queue(layer)
		self._push_layer_event_handlers(layer)

		if self._layer_supports_updating(layer):
			self._update_queue.append(layer)

	def _append_to_drawing_queue(self, layer):
		"""Adds a layer to the end of the drawing queue.

		If the layer supports batches, it will be added to a batch
		at the end of the queue. If the layer does not support batches,
		the layer itself will be added to the end of the queue and will
		be expected to draw itself.

		Args:
			layer (:class:`game.layers.basic_layer.BasicLayer`): The layer to append to the drawing queue.
		"""
		# If the layer supports batches, add it to the current batch in the drawing queue
		if layer.supports_batches():
			# If the current item in the drawing queue is not a batch, create a batch and add it to the queue
			if not self._drawing_queue or not isinstance(self._drawing_queue[-1], Batch):
				self._drawing_queue.append(Batch())

			# If the layer supports groups, order its rendering to the current depth
			if layer.supports_groups():
				layer.set_batch_and_group(self._drawing_queue[-1], OrderedGroup(self._depth))
				self._depth += 1 # Render the next layer at the next depth
			else:
				layer.set_batch(self._drawing_queue[-1])
		# If this layer doesn't support batches, it will be asked to draw itself
		else:
			self._drawing_queue.append(layer)

	def _push_layer_event_handlers(self, layer):
		"""Sets event handlers for when a layer dispatches an event.

		Args:
			layer (:class:`game.layers.basic_layer.BasicLayer`): The layer to set event handlers on.
		"""
		layer.set_handler('on_delete', self._on_layer_delete)

	def _on_layer_delete(self, layer):
		"""Event handler for when a layer is deleted.

		The layer will cease to be managed, and any adjacent batches
		in the drawing queue will be coalesced if the layer was
		responsible for drawing itself.

		Args:
			layer (:class:`game.layers.basic_layer.BasicLayer`): The layer which was deleted.
		"""
		# If the layer supported updating, remove it from the update queue
		if self._layer_supports_updating(layer):
			self._update_queue.remove(layer)

		# TODO If this was the only thing in its batch/group, delete the group
		# TODO If this didn't support batching, coalesce batches if possible
		if not layer.supports_batches():
			self._drawing_queue.remove(layer)

	def _layer_supports_updating(self, layer):
		"""Determines whether a layer can be updated by calling ``update`` on it.

		This is done by checking for an ``update`` method on the layer.

		Args:
			layer (:class:`game.layers.basic_layer.BasicLayer`): The layer to check for update support.

		Returns:
			True if the layer supports updating, False otherwise.
		"""
		return hasattr(layer, 'update')
