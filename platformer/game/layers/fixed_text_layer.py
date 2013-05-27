import fixed_layer

class FixedTextLayer(fixed_layer.FixedLayer):
	"""A layer of text content which remainds fixed relative to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedTextLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		# TODO If the Heading was on a timer, this object should delete itself when the timer ends
		self.graphic.update(x=self.viewport.x + self.offset_x, y=self.viewport.y + self.offset_y)

	# All text modules support batches
	def supports_batches(self):
		return True

	# All text modules support groups
	def supports_groups(self):
		return True
