import pyglet
from game import util
from game.tiles import tile_factory
from tile_map import TileMap
from ..settings.general_settings import TILE_SIZE

class TextureTileMap(TileMap):
	"""A grid of tiles which can be drawn efficiently.

	Attributes:
		tiles (2d lits of :class:`game.tiles.tile.Tile`): A 2d list of the tiles on the map. Empty tiles are represented as ``None``.
		texture (:class:`pyglet.image.Texture`): A texture containing the entire tile map image.
	"""

	def __init__(self, value_map, tile_image, rows=None, cols=None):
		"""Creates a new tile map.

		If ``rows`` and ``cols`` are not specified, they will be calculated from the
		size of the tile sprite image and the default tile size.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tile_image (str): The path to the tile sprite image.

		Kwargs:
			rows (int): The number of rows of tiles in the tile sprite file.
			cols (int): The number of columns of tiles in the tile sprite image.
		"""
		self.tiles = None
		self.texture = None

		# Create the stage map from the given level data
		self._create_tile_map(value_map, tile_image, image_rows=rows, image_cols=cols)

	def _create_tile_map(self, value_map, tile_image, image_rows=None, image_cols=None):
		"""Creates a 2d list of tile objects and a texture for the entire tile map.

		If ``image_rows`` and ``image_cols`` are not specified, they will be calculated from the
		size of the tile sprite image and the default tile size.

		Args:
			value_map (2d list of int): A 2d list of the tile values for each tile in the tile map.
			tile_image (str): The path to the tile sprite image.

		Kwargs:
			image_rows (int): The number of rows of tiles in the tile sprite file.
			image_cols (int): The number of columns of tiles in the tile sprite image.
		"""
		if not image_rows:
			image_rows = int(tile_image.width / TILE_SIZE)
		if not image_cols:
			image_cols = int(tile_image.height / TILE_SIZE)

		# Load the tile sprite and create a texture grid from it
		tile_image = pyglet.resource.image(tile_image)
		tileset = pyglet.image.TextureGrid(pyglet.image.ImageGrid(tile_image, image_rows, image_cols))

		# Cache of each tile image and its image data
		cached_tile_image = {}
		cached_image_data = {}

		# Get the number of columns and rows in the tile map
		cols = len(value_map) # Account for anchor points being on the bottom left
		rows = len(value_map[0])

		# Initialize an empty tile map
		self.tiles = [[None] * rows for i in xrange(cols)]

		# Create a texture for the entire tile map
		self.texture = pyglet.image.Texture.create(rows*TILE_SIZE, cols*TILE_SIZE)

		for y in xrange(cols):
			for x in xrange(rows):
				tile_value = value_map[y][x]

				if tile_value is not 0: # Ignore empty tiles
					# Adjust the y coordinate because the anchor point is at the bottom left
					adjusted_y = cols - y - 1
					coordinates = util.tile_to_coordinate(x, adjusted_y)

					# Get the indices of the tile piece we want in the tile image
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

					if tile_value not in cached_tile_image:
						cached_tile_image[tile_value] = tileset[row, col]
						cached_image_data[tile_value] = cached_tile_image[tile_value].get_image_data()

					# Create the tile and add it to the map
					self.tiles[adjusted_y][x] = tile_factory.create_tile(img=cached_tile_image[tile_value], x=coordinates[0], y=coordinates[1], **temp_tile_args)

					# Blit the tile image to the tile map texture
					cached_image_data[tile_value].blit_to_texture(self.texture.target, self.texture.level, coordinates[0], coordinates[1], 0)

	def draw(self, x, y):
		"""Draws the entire tile map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the tile map from.
			y (int): The y coordinate to draw the tile map from.
		"""
		self.texture.blit(x, y)

	def draw_region(self, x, y, width, height):
		"""Draws only a region of the texture map with its anchor point (usually the bottom left corner) at the given coordinates.

		Args:
			x (int): The x coordinate to draw the tile map region from.
			y (int): The y coordinate to draw the tile map from.
			width (int): The width of the tile map region to draw.
			height (int): The height of the tile map region to draw.
		"""
		self.texture.get_region(x, y, width, height).blit(x, y)
