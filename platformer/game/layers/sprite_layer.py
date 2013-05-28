import basic_layer

class SpriteLayer(basic_layer.BasicLayer):
	"""A layer which contains a :class:`pyglet.sprite.Sprite` as its content."""

	def __init__(self, *args, **kwargs):
		super(SpriteLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		"""Updates the layer's sprite.

		Args:
			dt (number): The time delta (in seconds) between the current frame and the previous frame.
		"""
		self.graphic.update(dt)
