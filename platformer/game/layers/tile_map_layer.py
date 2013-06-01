from basic_layer import BasicLayer

class TileMapLayer(BasicLayer):
	"""A layer which contains a :class:`game.tiles.tile_map.TileMap` as its content."""

	def draw(self):
		"""Draws only the visible region of the tile map."""
		self.graphic.draw_region(self.viewport.x, self.viewport.y, self.viewport.width, self.viewport.height)

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
