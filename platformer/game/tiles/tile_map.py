from game import util
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE

class TileMap(object):
	"""A grid of tiles.

	Useful for drawing tile-based environments.

	Attributes:
		tiles (2d list of :class:`game.tiles.tile.Tile`): 2d list of tiles on the map. Empty tiles are represented as ``None``.
		rows (int): The number of rows of tiles in the map.
		cols (int): The number of columns of tiles in the map.
	"""

	def __init__(self, value_map, tileset, batch=None, group=None):
		"""Creates a new tile map.

		Args:
			value_map (list of int): List of tile indices from the tile image.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.

		Kwargs:
			batch (:class:`pyglet.graphics.Batch`): A graphics batch to add each tile to.
			group (:class:`pyglet.graphics.Group`): A graphics group to add each tile to.
		"""
		# Pyglet graphics attributes
		self._batch = batch
		self._group = group

		self._visible_tiles = set()
		self._tile_objects = [] # List of all tile objects

		self.tiles = None
		self.rows = len(value_map[0])
		self.cols = len(value_map)

		# The maximum dimensions of this tile map
		self._max_dimensions = BoundedBox(
			0, 0, self.cols * TILE_SIZE, self.rows * TILE_SIZE
		)

		# The default visible area is the entire tile map
		self._visible_region = self._max_dimensions

		# Create the map from the given tile values and tileset
		self._create_tile_map(value_map, tileset)

	def _create_tile_map(self, value_map, tileset):
		"""Creates a 2d list of tile objects.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tileset (:class:`game.tiles.tileset.Tileset`): The tileset to use for the map.
		"""
		# Initialize an empty tile map
		self.tiles = [[None] * self.rows for i in xrange(self.cols)]

		for y in xrange(self.cols):
			for x in xrange(self.rows):
				tile_value = value_map[y][x]

				if tile_value is not 0: # Ignore empty tiles
					# Adjust the y coordinate for an anchor at the bottom left
					adjusted_y = self.cols-y-1
					coordinates = util.tile_to_coordinate(x, adjusted_y)

					self.tiles[adjusted_y][x] = tileset.create_tile(tile_value, x=coordinates[0], y=coordinates[1], batch=self._batch, group=self._group)

					self._tile_objects.append(self.tiles[adjusted_y][x])
					self._visible_tiles.add(self.tiles[adjusted_y][x])

	def draw(self):
		"""Draws the entire tile map."""
		self.draw_region(
			self._max_dimensions.x,		self._max_dimensions.y,
			self._max_dimensions.width,	self._max_dimensions.height
		)

	def draw_region(self, x, y, width, height):
		"""Draws a region of the tile map.

		Args:
			x (int): The x coordinate to draw the region from.
			y (int): The y coordinate to draw the region from.
			width (int): The width of the region to draw.
			height (int): The height of the region to draw.
		"""
		self.set_visible_region(x, y, width, height)
		self._batch.draw()

	# TODO Benchmark how much more efficient this actually is
	def set_visible_region(self, x, y, width, height):
		"""Sets the visible region of the tile map.

		Because invisible tiles are not drawn, this method can
		reduce the amount of drawing to do.

		Args:
			x (int): The x coordinate to draw the region from.
			y (int): The y coordinate to draw the region from.
			width (int): The width of the region to draw.
			height (int): The height of the region to draw.
		"""
		# Bound the region to the tile map's dimensions
		region = BoundedBox(x, y, width, height)
		region.bound_within(self._max_dimensions)

		# Do nothing if the requested region is the current visible region
		if region == self._visible_region:
			return

		# Keep track of the currently visible region
		self._visible_region = region

		# Create a list of all tiles in the region
		tiles_in_region = []
		for y in xrange(region.y_tile, region.y2_tile):
			for x in xrange(region.x_tile, region.x2_tile):
				tile = self.tiles[y][x]
				if tile:
					tile.visible = True
					tiles_in_region.append(tile)

		# Determine which tiles need to be made invisible
		make_invisible = self._visible_tiles.difference(tiles_in_region)
		map(lambda tile: tile.__setattr__('visible', False), make_invisible)

		# Keep track of which tiles are visible
		self._visible_tiles = set(tiles_in_region)



	@property
	def batch(self):
		"""Gets batch."""
		return self._batch

	@batch.setter
	def batch(self, batch):
		"""Sets the graphics batch for each tile in the map."""
		map(lambda tile: tile.__setattr__('batch', batch), self._tile_objects)
		self._batch = batch

	@property
	def group(self):
		"""Gets group."""
		return self._group

	@group.setter
	def group(self, group):
		"""Sets the graphics group for each tile in the map."""
		map(lambda tile: tile.__setattr__('group', group), self._tile_objects)
		self._group = group
