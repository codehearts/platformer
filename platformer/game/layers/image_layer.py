from base_layer import BaseLayer
from fixed_layer import FixedLayer

class StaticImageLayer(BaseLayer):
	"""A layer of static image content.

	The contents of this layer are never updated.

	This layer is intended for use with classes and subclasses from
	:mod:`pyglet.image` which are drawn via ``draw()`` and ``blit()``.
	"""

	def __init__(self, *args, **kwargs):
		super(StaticImageLayer, self).__init__(*args, **kwargs)

	def draw(self):
		"""Draws the contents of this layer.

		This is performed by calling ``self.graphic.blit(0, 0)``.
		"""
		self.graphic.blit(0, 0)



class ImageLayer(StaticImageLayer):
	"""An image layer that updates its contents each frame.

	Updating is performed by calling ``self.graphic.update(dt)``.
	If this won't work for your image object, you may want a subclass
	of this class.
	"""

	def __init__(self, *args, **kwargs):
		super(ImageLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		"""Updates the layer's contents.

		This is performed by calling ``self.graphic.update(dt)``.

		Args:
			dt (float): The number of seconds that elapsed between the last update.
		"""
		self.graphic.update(dt)



class FixedStaticImageLayer(FixedLayer, StaticImageLayer):
	"""A static image layer which remains fixed to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedStaticImageLayer, self).__init__(*args, **kwargs)

	def draw(self):
		"""Draws the layer's contents fixed to the viewport.

		This is performed by calling ``self.graphic.blit(x, y)``,
		where ``x`` and ``y`` are provided by the viewport and are
		offset by the amount specified when initializing this class.
		"""
		self.graphic.blit(self.viewport.x + self.offset_x, self.viewport.y + self.offset_y)



class FixedImageLayer(FixedStaticImageLayer, ImageLayer):
	"""An image layer which remains fixed to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedImageLayer, self).__init__(*args, **kwargs)



def recognizer(graphic):
	"""Recognizes whether this layer type supports the graphics object."""
	return hasattr(graphic, 'blit')

def factory(static=False, fixed=False):
	"""Returns the proper class for the given layer properties."""
	if static and fixed:
		return FixedStaticImageLayer

	if fixed:
		return FixedImageLayer

	if static:
		return StaticImageLayer

	return ImageLayer
