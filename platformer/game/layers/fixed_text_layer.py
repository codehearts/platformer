import fixed_layer, text_layer

class FixedTextLayer(fixed_layer.FixedLayer, text_layer.TextLayer):
	"""A layer of text content which remains fixed relative to the viewport."""

	def _update_graphic_coordinates(self, x, y, dt):
		self.graphic.update(x=self.viewport.x + self.offset_x, y=self.viewport.y + self.offset_y)
