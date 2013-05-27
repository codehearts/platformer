import basic_layer

class TileMapLayer(basic_layer.BasicLayer):
	# TODO Reference the full path of TileMap in the docstring
	"""A layer which contains a :class:`TileMap` as its content."""

	def __init__(self, *args, **kwargs):
		super(TileMapLayer, self).__init__(*args, **kwargs)

	# All TileMaps support batches
	def supports_batches(self):
		return True

	# All TileMaps support groups
	def supports_groups(self):
		return True

	def set_batch(self, batch):
		self.graphic.set_batch(batch)

	def set_group(self, group):
		self.graphic.set_group(group)
