from graphics_layer import GraphicsLayer
from ..tiles import TileMap

class TileMapLayer(GraphicsLayer):
	"""A layer which contains a :class:`game.tiles.TileMap`."""

	def update(self, dt):
		"""Sets the visible region of the map to the viewport's region."""
		self.graphic.set_visible_region(self.viewport.x, self.viewport.y, self.viewport.width, self.viewport.height)

# TODO Subclass with FixedGraphicsLayer for a fixed tile map layer



def recognizer(graphic):
	"""Recognizes whether this layer type supports the graphics object."""
	return isinstance(graphic, TileMap)

def factory(**kwargs):
	"""Returns the proper class for the given layer properties."""
	return TileMapLayer
