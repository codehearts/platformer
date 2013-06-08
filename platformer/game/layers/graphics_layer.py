from base_layer import BaseLayer
from fixed_layer import FixedLayer

class StaticGraphicsLayer(BaseLayer):
	"""A layer of static graphics content.

	The contents of this layer are never updated.

	This layer is intended for use with classes and subclasses from
	:mod:`pyglet.graphics` which make use of graphics batches and groups.

	Attributes:
		batch (:class:`pyglet.graphics.Batch`): A graphics batch for the layer's contents.
		group (:class:`pyglet.graphics.Group`): A graphics group for the layer's contents.
	"""

	def __init__(self, *args, **kwargs):
		super(StaticGraphicsLayer, self).__init__(*args, **kwargs)

	@property
	def batch(self):
		"""Gets batch."""
		return self.graphic.batch

	@batch.setter
	def batch(self, batch):
		"""Adds the layer's graphical content to the given batch.

		Args:
			batch (:class:`pyglet.batch.Batch`): The batch to add the layer's graphical content to.
		"""
		self.graphic.batch = batch

	@property
	def group(self):
		"""Gets group."""
		return self.graphic.group

	@group.setter
	def group(self, group):
		"""Adds the layer's graphical content to the given group.

		Args:
			group (:class:`pyglet.graphics.Group`): The group to add the layer's graphical content to.
		"""
		self.graphic.group = group

	def delete(self, *args, **kwargs):
		"""Deletes the layer.

		Graphics layer deletion is performed by removing the
		layer's graphical content from its batch and group.
		"""
		self.graphic.group = None
		self.graphic.delete()
		super(StaticGraphicsLayer, self).delete(*args, **kwargs)



class GraphicsLayer(StaticGraphicsLayer):
	"""A graphics layer that updates its contents each frame.

	Updating is performed by calling ``self.graphic.update(dt)``.
	If this won't work for your graphics object, you may want a subclass
	of this class.
	"""
	def __init__(self, *args, **kwargs):
		super(GraphicsLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		"""Updates the layer's contents.

		This is performed by calling ``self.graphic.update(dt)``.

		Args:
			dt (float): The number of seconds that elapsed between the last update.
		"""
		self.graphic.update(dt)



class FixedStaticGraphicsLayer(FixedLayer, StaticGraphicsLayer):
	"""A static graphics layer which remains fixed to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedStaticGraphicsLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		"""Updates the layer's contents to be fixed to the viewport."""
		self.fix_graphic()



class FixedGraphicsLayer(FixedLayer, GraphicsLayer):
	"""A graphics layer which remains fixed to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedGraphicsLayer, self).__init__(*args, **kwargs)

	def update(self, *args, **kwargs):
		"""Updates the layer's contents to be fixed to the viewport."""
		self.fix_graphic()
		super(FixedGraphicsLayer, self).update(*args, **kwargs)



def recognizer(graphic):
	"""Recognizes whether this layer type supports the graphics object."""
	return hasattr(graphic, 'batch')

def factory(static=False, fixed=False):
	"""Returns the proper class for the given layer properties."""
	if static and fixed:
		return FixedStaticGraphicsLayer

	if fixed:
		return FixedGraphicsLayer

	if static:
		return StaticGraphicsLayer

	return GraphicsLayer
