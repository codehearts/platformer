import basic_layer

# Layer which remains fixed relative to the viewport
class FixedLayer(basic_layer.BasicLayer):

	def __init__(self, *args, **kwargs):
		super(FixedLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		self.image.x = self.viewport.x
		self.image.y = self.viewport.y
