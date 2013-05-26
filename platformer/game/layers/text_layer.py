import fixed_layer

class TextLayer(fixed_layer.FixedLayer):

	def __init__(self, *args, **kwargs):
		super(TextLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		# TODO If the Heading was on a timer, this object should delete itself when the timer ends
		self.graphic.update(dt, x=self.viewport.x + self.offset_x, y=self.viewport.y + self.offset_y)

	# All text modules support batches
	def supports_batches(self):
		return True

	def set_batch(self, new_batch):
		self.graphic.set_batch(new_batch)
