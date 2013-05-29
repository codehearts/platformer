import basic_layer

class AnimationLayer(basic_layer.BasicLayer):
	"""A layer of animated graphical content.

	Attributes:
		on_animation_end (function): Callback function for when the animation ends.
	"""

	def __init__(self, *args, **kwargs):
		"""
		Args:
			graphic (:class:`game.animation.basic_animation.BasicAnimation`): The animation to draw on the layer.

		Kwargs:
			on_animation_end (function): Callback function for when the animation ends. The function should accept the animation as its first argument and the layer as its second.
		"""
		self.on_animation_end = kwargs.pop('on_animation_end', None)
		super(AnimationLayer, self).__init__(*args, **kwargs)

		self.graphic.set_handler('on_animation_end', self._on_animation_end)

	def update(self, dt):
		self.graphic.update(dt)

	def _on_animation_end(self, animation):
		"""Event handler for when the animation ends.

		This is done by calling the ``on_animation_end`` attribute
		with the animation as its first parameter and the layer
		as its second.

		Args:
			animation (:class:`game.animation.basic_animation.BasicAnimation`): The animation that ended.
		"""
		if self.on_animation_end:
			self.on_animation_end(animation, self)
