from image_layer import ImageLayer, FixedImageLayer
from ..animation import BasicAnimation

class AnimationLayer(ImageLayer):
	"""A layer with animated content.

	Attributes:
		on_animation_end (function): Callback function for when the animation ends.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Args:
			graphic (:class:`game.animation.BasicAnimation`): The animation.

		Kwargs:
			on_animation_end (function): Callback function for when the animation ends. The function should accept the animation as its first argument and the layer as its second.
		"""
		on_animation_end = kwargs.pop('on_animation_end', None)
		super(AnimationLayer, self).__init__(*args, **kwargs)

		if on_animation_end:
			self._on_animation_end_callback = on_animation_end
			self.graphic.set_handler('on_animation_end', self._on_animation_end)

	def _on_animation_end(self, animation):
		"""Calls the given on_animation_end callback.

		The callback function should accept the animation as its first
		argument and the layer as its second.

		Args:
			animation (:class:`game.animation.BasicAnimation`): The animation which fired the on_animation_end event.
		"""
		self._on_animation_end_callback(animation, self)



class FixedAnimationLayer(AnimationLayer, FixedImageLayer):
	"""A layer with animated content fixed relative to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedAnimationLayer, self).__init__(*args, **kwargs)



def recognizer(graphic):
	"""Recognizes whether this layer type supports the graphics object."""
	return isinstance(graphic, BasicAnimation)

def factory(fixed=False, **kwargs):
	"""Returns the proper class for the given layer properties."""
	if fixed:
		return FixedAnimationLayer

	return AnimationLayer
