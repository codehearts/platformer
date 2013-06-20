from game import util
from game.bounded_box import BoundedBox
from pyglet.image import Texture
from ..settings.general_settings import TILE_SIZE

class TextureTileMap(object):
	"""A grid of tiles which can be drawn efficiently.

	Attributes:
		tiles (2d list of :class:`game.tiles.tile.Tile`): A 2d list of the tiles on the map. Empty tiles are represented as ``None``.
		rows (int): The number of rows of tiles in the map.
		cols (int): The number of columns of tiles in the map.
		texture (:class:`pyglet.image.Texture`): A texture containing the entire tile map image.
	"""

	def __init__(self, value_map, tileset):
		"""Creates a new tile map.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		self.rows = len(value_map)
		self.cols = len(value_map[0])
		self.tiles = None
		self.texture = None

		# The maximum dimensions of this tile map
		self._max_dimensions = BoundedBox(
			0, 0, self.cols * TILE_SIZE, self.rows * TILE_SIZE
		)

		# Create the map from the given tile values and tileset
		self._create_tile_map(value_map, tileset)

	def _create_tile_map(self, value_map, tileset):
		"""Creates a 2d list of tile objects and a texture for the entire tile map.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		# Initialize an empty tile map
		self.tiles = [[None] * self.cols for i in xrange(self.rows)]

		# Create the texture for the tile map
		self.texture = Texture.create(self._max_dimensions.width, self._max_dimensions.height)

		for y in xrange(self.rows):
			for x in xrange(self.cols):
				tile_value = value_map[y][x]

				if tile_value != 0: # Ignore empty tiles
					# Adjust the y coordinate because the anchor point is at the bottom left
					adjusted_y = self.rows - y - 1
					coords = util.tile_to_coordinate(x, adjusted_y)

					# Create the tile and add it to the map
					self.tiles[adjusted_y][x] = tileset.create_tile(tile_value, x=coords[0], y=coords[1])

					# Blit the tile image to the map texture
					self.texture.blit_into(tileset.image.get_tile_image_data(tile_value), coords[0], coords[1], 0)
					#tileset.image.get_tile_image_data(tile_value).blit_to_texture(self.texture.target, self.texture.level, coords[0], coords[1], 0)

	def blit(self, x, y):
		"""Draws the entire tile map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the tile map from.
			y (int): The y coordinate to draw the tile map from.
		"""
		self.texture.blit(x, y)

	# TODO Accept a BoundedBox as the argument
	def get_region(self, x, y, width, height):
		"""Returns a region of the tile map.

		Args:
			x (int): The x coordinate of the region.
			y (int): The y coordinate of the region.
			width (int): The width of the region.
			height (int): The height of the region.

		Returns:
			A :class:`game.extended_texture.ExtendedTextureRegion` object.
		"""
		region = BoundedBox(x - self.texture.anchor_x, y - self.texture.anchor_y, width, height)
		region = region.get_intersection(self._max_dimensions)

		return self.texture.get_region(
			region.x, region.y, region.width, region.height
		)

	def blit_region(self, x, y, width, height):
		"""Draws a region of the tile map.

		Args:
			x (int): The x coordinate to draw the region from.
			y (int): The y coordinate to draw the region from.
			width (int): The width of the region to draw.
			height (int): The height of the region to draw.
		"""
		# Bound the drawn region to the texture's dimensions
		region = self.get_region(x, y, width, height)
		region.blit(region.x + self.texture.anchor_x, region.y + self.texture.anchor_y)


	def _set_x(self, x):
		self.texture.anchor_x = x
		self._max_dimensions._set_x(x)

	x = property(lambda self: self.texture.anchor_x, _set_x)


	def _set_y(self, y):
		self.texture.anchor_y = y
		self._max_dimensions._set_y(y)

	y = property(lambda self: self.texture.anchor_y, _set_y)
