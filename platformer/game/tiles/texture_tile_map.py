from game import util
from pyglet.image import Texture
from tile_map import TileMap
from ..settings.general_settings import TILE_SIZE

class TextureTileMap(TileMap):
	"""A grid of tiles which can be drawn efficiently.

	Attributes:
		tiles (2d list of :class:`game.tiles.tile.Tile`): A 2d list of the tiles on the map. Empty tiles are represented as ``None``.
		texture (:class:`pyglet.image.Texture`): A texture containing the entire tile map image.
	"""

	def __init__(self, value_map, tileset):
		"""Creates a new tile map.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		self.tiles = None
		self.texture = None

		# Create the map from the given tile values and tileset
		self._create_tile_map(value_map, tileset)

	def _create_tile_map(self, value_map, tileset):
		"""Creates a 2d list of tile objects and a texture for the entire tile map.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		# Get the number of rows and columns for the tile map
		rows = len(value_map[0])
		cols = len(value_map)

		# Initialize an empty tile map
		self.tiles = [[None] * rows for i in xrange(cols)]

		# Create the texture for the tile map
		self.texture = Texture.create(rows*TILE_SIZE, cols*TILE_SIZE)

		for y in xrange(cols):
			for x in xrange(rows):
				tile_value = value_map[y][x]

				if tile_value is not 0: # Ignore empty tiles
					# Adjust the y coordinate because the anchor point is at the bottom left
					adjusted_y = cols - y - 1
					coords = util.tile_to_coordinate(x, adjusted_y)

					# Create the tile and add it to the map
					self.tiles[adjusted_y][x] = tileset.create_tile(tile_value, x=coords[0], y=coords[1])

					# Blit the tile image to the map texture
					tileset.image.get_tile_image_data(tile_value).blit_to_texture(self.texture.target, self.texture.level, coords[0], coords[1], 0)

	def draw(self, x, y):
		"""Draws the entire tile map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the tile map from.
			y (int): The y coordinate to draw the tile map from.
		"""
		self.texture.blit(x, y)

	def draw_region(self, x, y, width, height):
		"""Draws a region of the texture map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the region from.
			y (int): The y coordinate to draw the region from.
			width (int): The width of the region to draw.
			height (int): The height of the region to draw.
		"""
		# TODO If the region goes beyond the texture, the texture repeats. Try not to do this!
		self.texture.get_region(x, y, width, height).blit(x, y)
