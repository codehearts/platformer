from image_layer import StaticImageLayer
from fixed_layer import FixedLayer
from ..tiles import TextureTileMap

class TextureTileMapLayer(StaticImageLayer):
	"""A layer which contains a :class:`game.tiles.TextureTileMap`."""

	def __init__(self, *args, **kwargs):
		super(TextureTileMapLayer, self).__init__(*args, **kwargs)

	def draw(self):
		"""Draw the visible region of the tile map."""
		self.graphic.blit_region(self.viewport.x, self.viewport.y, self.viewport.width, self.viewport.height)



class FixedTextureTileMapLayer(FixedLayer, TextureTileMapLayer):
	"""A texture tile map layer which remains fixed to the viewport."""

	def __init__(self, *args, **kwargs):
		super(FixedTextureTileMapLayer, self).__init__(*args, **kwargs)

	def draw(self):
		"""Draws the tile map fixed to the viewport.

		This is performed by setting ``anchor_x`` and ``anchor_y`` on the
		tile map and then blitting it relative to the viewport.

		Only the visible region of the tile map is drawn.
		"""
		self.fix_graphic()
		self.graphic.blit_region(self.viewport.x + self.offset_x, self.viewport.y + self.offset_y, self.viewport.width, self.viewport.height)



def recognizer(graphic):
	"""Recognizes whether this layer type supports the graphics object."""
	return isinstance(graphic, TextureTileMap)

def factory(fixed=False, **kwargs):
	"""Returns the proper class for the given layer properties."""
	if fixed:
		return FixedTextureTileMapLayer

	return TextureTileMapLayer
