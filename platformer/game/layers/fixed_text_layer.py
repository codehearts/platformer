import fixed_layer

class FixedTextLayer(fixed_layer.FixedLayer):
	"""A layer of text content which remains fixed relative to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedTextLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		self.graphic.update(x=self.viewport.x + self.offset_x, y=self.viewport.y + self.offset_y)

	# All text modules support batches
	def supports_batches(self):
		return True

	# All text modules support groups
	def supports_groups(self):
		return True

	def set_batch(self, batch):
		self.graphic.begin_update()
		self.graphic.batch = batch
		self.graphic.end_update()

	def set_group(self, group):
		self.graphic.begin_update()
		self.graphic.group = group
		self.graphic.end_update()

	def set_batch_and_group(self, batch, group):
		self.graphic.begin_update()
		self.graphic.batch = batch
		self.graphic.group = group
		self.graphic.end_update()
