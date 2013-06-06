import animation_layer, fixed_layer

class FixedAnimationLayer(fixed_layer.FixedLayer, animation_layer.AnimationLayer):
	"""A layer of animated graphical content which remains fixed relative to the viewport."""

	def update(self, dt):
		self.graphic.update(dt)

	def draw(self):
		self.graphic.draw(self.viewport.x + self.offset_x, self.viewport.y + self.offset_y)
