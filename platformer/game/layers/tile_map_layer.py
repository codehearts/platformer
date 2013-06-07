from graphics_layer import GraphicsLayer

class TileMapLayer(GraphicsLayer):
	"""A layer which contains a :class:`game.tiles.TileMap`."""

	def update(self, dt):
		"""Sets the visible region of the map to the viewport's region."""
		self.graphic.set_visible_region(self.viewport.x, self.viewport.y, self.viewport.width, self.viewport.height)

# TODO Subclass with FixedGraphicsLayer for a fixed tile map layer
