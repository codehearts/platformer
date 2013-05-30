import pyglet
from game import tile, util
from ..settings import general_settings, tile_settings

# TODO Offscreen tiles could be culled by setting their `visible` attribute to False (check if this improves performance at all)
# TODO A subclass should be made which uses a texture for everything
class TileMap(object):

	# Needs an array of tile values (tile value map)
	# Needs optional dimensions, or defaults to size of tile value map
	# Needs tile sprite file
	# Needs tile type assignments
	def __init__(self, value_map, tile_image, rows=None, cols=None):
		self.batch = pyglet.graphics.Batch()
		self.tiles = [] # Map of all tile objects

		# Create the stage map from the given level data
		self._create_tile_map(value_map, tile_image, rows=None, cols=None)

	# TODO Instead of adding each tile object to a batch and drawing that, this could be drawn as a single texture, and only the region visible by the viewport is drawn
	# TODO When initializing, a single tile could be made for each tile_value and then blitted into the tilemap texture
	# Create the stage map as a 2d array of tile objects indexed with an anchor point at the bottom left
	# The level data is expected to have a stage_map property that is a 2d array of numeric tile values
	def _create_tile_map(self, value_map, tile_image, image_rows=None, image_cols=None):
		if not image_rows:
			image_rows = int(tile_image.width / general_settings.TILE_SIZE)
		if not image_cols:
			image_cols = int(tile_image.height / general_settings.TILE_SIZE)

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

					# Determine whether this is a special tile
					tile_type = tile_settings.NORMAL
					for tile_key, special_values in level_data.get_tile_type_assignments().iteritems():
						if tile_value in special_values:
							tile_type = tile_key

					# TODO Need a way to tell which tile object to get

					self.tiles[adjusted_y][x] = tile.Tile(img=tileset[row, col], x=coordinates[0], y=coordinates[1], tile_type=tile_type, batch=self.batch)

	# Returns a 2d array of all tile objects on the stage
	def get_tiles(self):
		return self.tiles

	# Draw the stage to the screen
	def draw(self):
		self.batch.draw()

	def set_batch(self, batch):
		# TODO There should be a list of actual tile object references (list of tiles excluding None values) to make these loops faster
		# Loop through each tile and set its batch attribute to the given batch if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('batch', batch), row), self.tiles)

	def set_group(self, group):
		# TODO There should be a list of actual tile object references (list of tiles excluding None values) to make these loops faster
		# Loop through each tile and set its group attribute to the given group if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('group', group), row), self.tiles)

	# TODO A get_region method could be useful for setting the visibility of onscreen and offscreen tiles
