import basic_layer

class TextLayer(basic_layer.BasicLayer):
	"""A layer of text content."""

	def __init__(self, *args, **kwargs):
		super(TextLayer, self).__init__(*args, **kwargs)

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
