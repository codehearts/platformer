class BasicLayer(object):
	"""A layer of graphical content which can be drawn with other layers in a specific order when passed to a :class:`layers.layer_manager.LayerManager` object.

	Attributes:
		graphic: The graphical content of this layer.
		viewport: The viewport that this layer will be viewed through.
	"""

	def __init__(self, graphic, viewport):
		"""Creates a new layer.

		Args:
			graphic: The graphical content for this layer.
			viewport: The viewport that this layer will be viewed through. The viewport should have ``x`` and ``y`` attributes.
		"""
		self.graphic = graphic
		self.viewport = viewport

	def update(self, dt):
		"""Updates the layer's graphical content.

		Args:
			dt: The time delta (in seconds) between the current frame and the previous frame.
		"""
		pass

	def draw(self):
		"""Draws the layer's graphical content."""
		print "draw"
		self.graphic.draw()

	def supports_batches(self):
		"""Returns whether this layer's graphical content supports batches by checking if it has a ``batch`` attribute.

		Returns:
			True if this layer's graphical content has a ``batch`` attribute, False otherwise.
		"""
		return hasattr(self.graphic, 'batch')

	def supports_groups(self):
		"""Returns whether this layer's graphical content supports groups by checking if it has a ``group`` attribute.

		Returns:
			True if this layer's graphical content has a ``batch`` attribute, False otherwise.
		"""
		return hasattr(self.graphic, 'group')

	def set_batch(self, batch):
		"""Adds this layer's graphical content to the given batch.

		Args:
			batch (:class:`pyglet.batch.Batch`): The batch to add this layer's graphical content to.
		"""
		if self.supports_batches():
			self.graphic.batch = batch

	# TODO Should add support for setting batch and group at once (this is actually more efficient for text, which sanwiches these updates between a start() and end() call)
	def set_group(self, group):
		"""Adds this layer's graphical content to the given group.

		Args:
			group (:class:`pyglet.graphics.Group`): The group to add this layer's graphical content to.
		"""
		if self.supports_batches():
			self.graphic.group = group
