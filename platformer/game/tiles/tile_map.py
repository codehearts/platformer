import pyglet
from game import util

# TODO Offscreen tiles could be culled by setting their `visible` attribute to False (check if this improves performance at all)
class TileMap(object):
	"""A grid of tiles.

	Useful for drawing tile-based environments.

	Attributes:
		tiles (2d list of :class:`game.tiles.tile.Tile`): 2d list of tiles on the map. Empty tiles are represented as ``None``.
	"""

	def __init__(self, value_map, tileset):
		"""Creates a new tile map.

		Args:
			value_map (list of int): List of tile indices from the tile image.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		self._batch = pyglet.graphics.Batch()
		self.tiles = []

		# Create the map from the given tile values and tileset
		self._create_tile_map(value_map, tileset)

	def _create_tile_map(self, value_map, tileset):
		"""Creates a 2d list of tile objects.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		# Get the number of rows and columns for the tile map
		rows = len(value_map[0])
		cols = len(value_map)

		# Initialize an empty tile map
		self.tiles = [[None] * rows for i in xrange(cols)]

		for y in xrange(cols):
			for x in xrange(rows):
				tile_value = value_map[y][x]

				if tile_value is not 0: # Ignore empty tiles
					# Adjust the y coordinate for an anchor at the bottom left
					adjusted_y = cols-y-1
					coordinates = util.tile_to_coordinate(x, adjusted_y)

					self.tiles[adjusted_y][x] = tileset.create_tile(tile_value, x=coordinates[0], y=coordinates[1], batch=self._batch)

	# Returns a 2d array of all tile objects on the stage
	# TODO Remove all calls to this method and delete it in favor of accessing the attribute directly
	def get_tiles(self):
		return self.tiles

	def draw(self):
		"""Draws the entire tile map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the tile map from.
			y (int): The y coordinate to draw the tile map from.
		"""
		self._batch.draw()

	# TODO Actually set the visibility of onscreen and offscreen tiles according to the region
	def draw_region(self, x, y, width, height):
		"""Draws a region of the texture map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the region from.
			y (int): The y coordinate to draw the region from.
			width (int): The width of the region to draw.
			height (int): The height of the region to draw.
		"""
		self.draw()

	def set_batch(self, batch):
		# TODO There should be a list of actual tile object references (list of tiles excluding None values) to make these loops faster
		# Loop through each tile and set its batch attribute to the given batch if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('batch', batch), row), self.tiles)
		self._batch = batch

	def set_group(self, group):
		# TODO There should be a list of actual tile object references (list of tiles excluding None values) to make these loops faster
		# Loop through each tile and set its group attribute to the given group if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('group', group), row), self.tiles)
