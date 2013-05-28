from pyglet.clock import schedule_once
from pyglet.event import EventDispatcher

class BasicLayer(EventDispatcher):
	# TODO Put full path of LayerManager class in docstring
	"""A layer of graphical content which can be drawn with other layers in a specific order when passed to a :class:`layers.layer_manager.LayerManager` object.

	If a duration is given, the layer will be drawn for that amount of time and then deleted.

	Attributes:
		graphic (object): The graphical content of the layer.
		viewport (object): The viewport that the layer will be viewed through.
		duration (number): The number of seconds the layer should be drawn for before deleting itself.
	"""

	def __init__(self, graphic, viewport, duration=None):
		"""Creates a new layer.

		Args:
			graphic (object): The graphical content for the layer.
			viewport (object): The viewport that the layer will be viewed through. The viewport should have ``x`` and ``y`` attributes.
			duration (number): The number of seconds the layer should be drawn for before deleting itself.
		"""
		self.graphic = graphic
		self.viewport = viewport
		self.duration = duration

		if duration:
			schedule_once(self._handle_duration_end, duration)

	def draw(self):
		"""Draws the layer's graphical content."""
		self.graphic.draw()

	def supports_batches(self):
		"""Returns whether the layer's graphical content supports batches.

		For a :class:`game.layers.basic_layer.BasicLayer`, this is done by checking for a ``batch`` attribute.

		Returns:
			True if the layer's graphical content supports batches, False otherwise.
		"""
		return hasattr(self.graphic, 'batch')

	def supports_groups(self):
		"""Returns whether the layer's graphical content supports groups.

		For a :class:`game.layers.basic_layer.BasicLayer`, this is done by checking for a ``group`` attribute.

		Returns:
			True if the layer's graphical content supports groups, False otherwise.
		"""
		return hasattr(self.graphic, 'group')

	# TODO Can't you listen for the batch attribute being set directly? Should I do that instead of this?
	def set_batch(self, batch):
		"""Adds the layer's graphical content to the given batch.

		Args:
			batch (:class:`pyglet.batch.Batch`): The batch to add the layer's graphical content to.
		"""
		if self.supports_batches():
			self.graphic.batch = batch

	# TODO Should add support for setting batch and group at once (this is actually more efficient for text, which sanwiches these updates between a start() and end() call)
	# TODO Can't you listen for the group attribute being set directly? Should I do that instead of this?
	def set_group(self, group):
		"""Adds the layer's graphical content to the given group.

		Args:
			group (:class:`pyglet.graphics.Group`): The group to add the layer's graphical content to.
		"""
		if self.supports_groups():
			self.graphic.group = group

	def set_batch_and_group(self, batch, group):
		self.set_batch(batch)
		self.set_group(group)

	def remove_batch(self):
		"""Removes the layer's graphical content from its current batch."""
		if self.supports_batches():
			self.graphic.delete()

	def remove_group(self):
		"""Removes the layer's graphical content from its current group."""
		if self.supports_groups():
			self.set_group(None)

	def delete(self):
		"""Deletes the current layer.

		Deletion is performed by removing the layer's graphical content from its batch and group. An ``on_delete`` event is also dispatched.
		"""
		# Remove the graphical content from its batch and group
		self.remove_group()
		self.remove_batch()
		self.dispatch_event('on_delete', self)

	def _handle_duration_end(self, dt):
		"""Deletes the current layer after its draw duration has elapsed.

		Args:
			dt (number): The amount of time (in seconds) that elapsed before this method was called."""
		self.delete()

# Register layer events
BasicLayer.register_event_type('on_delete')
