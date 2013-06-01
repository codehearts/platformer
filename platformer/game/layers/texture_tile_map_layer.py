from tile_map_layer import TileMapLayer

# TODO When TextureTileMap is refactored into TileMap, update the docstring
class TextureTileMapLayer(TileMapLayer):
	"""A layer which contains a :class:`game.tiles.texture_tile_map.TextureTileMap` as its content."""

	# TextureTileMaps do not support batches
	def supports_batches(self):
		return False

	# TextureTileMaps do not support groups
	def supports_groups(self):
		return False
