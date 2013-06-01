import pyglet
from game import util
from game.tiles import tile_factory
from ..settings.general_settings import TILE_SIZE

# TODO Offscreen tiles could be culled by setting their `visible` attribute to False (check if this improves performance at all)
# TODO Documentation!
# TODO Add methods for getting a tile's neighbors (tile_map.get_left(tile), tile_map.get_top_left(tile))
class TileMap(object):
	"""A grid of tiles.

	Useful for drawing tile-based environments.

	Attributes:
		tiles (2d list of :class:`game.tiles.tile.Tile`): 2d list of tiles on the map. Empty tiles are represented as ``None``.
	"""

	def __init__(self, value_map, tile_image, rows=None, cols=None):
		"""Creates a new tile map.

		If rows and columns aren't specified, they will be calculated using the
		size of the tile image and the default tile size.

		Args:
			value_map (list of int): List of tile indices from the tile image.
			tile_image (:class:`pyglet.image.AbstractImage`): Sprite image containing artwork for each tile.

		Kwargs:
			rows (int): The number of rows of tile artwork in the tile image.
			cols (int): The number of columns of tile artwork in the tile image.
		"""
		self._batch = pyglet.graphics.Batch()
		self.tiles = []

		# Create the stage map from the given level data
		self._create_tile_map(value_map, tile_image, image_rows=rows, image_cols=cols)

	# Create the stage map as a 2d array of tile objects indexed with an anchor point at the bottom left
	# The level data is expected to have a stage_map property that is a 2d array of numeric tile values
	def _create_tile_map(self, value_map, tile_image, image_rows=None, image_cols=None):
		if not image_rows:
			image_rows = int(tile_image.width / TILE_SIZE)
		if not image_cols:
			image_cols = int(tile_image.height / TILE_SIZE)

		self.tiles[:] = [[None] * len(value_map[0]) for i in xrange(len(value_map))] # Initiate an empty stage

		# Load the tile sprite and create a texture grid from it
		tile_image = pyglet.resource.image(tile_image)
		tileset = pyglet.image.TextureGrid(pyglet.image.ImageGrid(tile_image, image_rows, image_cols))

		# Get the number of columns and rows in the stage map
		cols = len(value_map) # Account for anchor points being on the bottom left
		rows = len(value_map[0])

		for y in xrange(cols):
			for x in xrange(rows):
				tile_value = value_map[y][x]

				if tile_value != 0: # Ignore empty tiles
					# Adjust the y coordinate for an anchor at the bottom left
					adjusted_y = cols-y-1
					coordinates = util.tile_to_coordinate(x, adjusted_y)

					# Index of the tile piece we want
					row = ((tile_value-1) / image_cols)
					col = tile_value - row * image_cols - 1
					row = image_rows - row - 1 # Adjust for index 0 being at the bottom left

					# TODO This should not be hardcoded here. There should be a config file for each tile sprite that gets read.
					temp_tile_args = {}
					if tile_value is 9:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 0
						temp_tile_args['right_height'] = 32
					elif tile_value is 10:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 32
						temp_tile_args['right_height'] = 0
					elif tile_value is 13:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 0
						temp_tile_args['right_height'] = 16
					elif tile_value is 14:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 17
						temp_tile_args['right_height'] = 32
					elif tile_value is 15:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 32
						temp_tile_args['right_height'] = 17
					elif tile_value is 16:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 16
						temp_tile_args['right_height'] = 0
					elif tile_value is 18:
						temp_tile_args['type'] = 'slope'
						temp_tile_args['left_height'] = 0
						temp_tile_args['right_height'] = 32
						temp_tile_args['is_ceiling'] = True

					self.tiles[adjusted_y][x] = tile_factory.create_tile(img=tileset[row, col], x=coordinates[0], y=coordinates[1], batch=self._batch, **temp_tile_args)

	# Returns a 2d array of all tile objects on the stage
	# TODO Remove all calls to this method and delete it in favor of accessing the attribute directly
	def get_tiles(self):
		return self.tiles

	# Draw the map
	def draw(self):
		self._batch.draw()

	def set_batch(self, batch):
		# TODO There should be a list of actual tile object references (list of tiles excluding None values) to make these loops faster
		# Loop through each tile and set its batch attribute to the given batch if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('batch', batch), row), self.tiles)
		self._batch = batch

	def set_group(self, group):
		# TODO There should be a list of actual tile object references (list of tiles excluding None values) to make these loops faster
		# Loop through each tile and set its group attribute to the given group if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('group', group), row), self.tiles)

	# TODO A get_region method could be useful for setting the visibility of onscreen and offscreen tiles
	def draw_region(self, x, y, width, height):
		self.draw()
