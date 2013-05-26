import basic_layer

class AnimationLayer(basic_layer.BasicLayer):
	"""A layer of animated graphical content."""

	def __init__(self, *args, **kwargs):
		super(AnimationLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		self.graphic.update(dt)
