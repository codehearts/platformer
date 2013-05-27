import pyglet
from game import tile, util
from ..settings import tile_settings

# TODO This could really be a general purpose TileMap class
class Stage(object):

	def __init__(self, level_data):
		self.batch = pyglet.graphics.Batch()
		self.tiles = [] # Map of all tile objects
		self.tile_map = [] # Map of all numeric tile values

		# Create the stage map from the given level data
		self.create_tile_map(level_data)

	# TODO This method could probably be moved out to its own file, possibly as a static class method
	# Create the stage map as a 2d array of tile objects indexed with an anchor point at the bottom left
	# The level data is expected to have a stage_map property that is a 2d array of numeric tile values
	def create_tile_map(self, level_data):
		stage_map = level_data.get_stage_map() # Store the stage map locally
		stage_size = level_data.get_stage_size() # Store the dimensions of the stage locally

		self.tiles[:] = [[None] * len(stage_map[0]) for i in xrange(len(stage_map))] # Initiate an empty stage
		self.tile_map[:] = [[0] * len(stage_map[0]) for i in xrange(len(stage_map))] # Initiate an empty stage

		# Load the tile sprite and create a texture grid from it
		tile_image = pyglet.resource.image(level_data.get_tile_sprite_file())
		tileset = pyglet.image.TextureGrid(pyglet.image.ImageGrid(tile_image, stage_size[0], stage_size[1]))

		# Get the number of columns and rows in the stage map
		cols = len(stage_map) # Account for anchor points being on the bottom left
		rows = len(stage_map[0])

		for y in xrange(cols):
			for x in xrange(rows):
				tile_value = stage_map[y][x]

				if tile_value != 0: # Ignore empty tiles
					# Adjust the y coordinate for an anchor at the bottom left
					adjusted_y = cols-y-1
					coordinates = util.tile_to_coordinate(x, adjusted_y)

					# Index of the tile piece we want
					row = ((tile_value-1) / stage_size[1])
					col = tile_value - row * stage_size[1] - 1
					row = stage_size[0] - row - 1 # Adjust for index 0 being at the bottom left

					# Determine whether this is a special tile
					tile_type = tile_settings.NORMAL
					for tile_key, special_values in level_data.get_tile_type_assignments().iteritems():
						if tile_value in special_values:
							tile_type = tile_key

					# TODO A smart thing to do would be to reuse tile image objects whenever possible
					self.tile_map[adjusted_y][x] = tile_value
					self.tiles[adjusted_y][x] = tile.Tile(img=tileset[row, col], x=coordinates[0], y=coordinates[1], tile_type=tile_type, batch=self.batch)

	# Returns a 2d array of all tile objects on the stage
	def get_tiles(self):
		return self.tiles

	# Returns a 2d array of the numeric tile values of each tile on the stage
	# TODO Why does this array exist?
	def get_tile_map(self):
		return self.tile_map

	# Draw the stage to the screen
	def draw(self):
		self.batch.draw()

	def set_batch(self, batch):
		# TODO There should be a list of actual tile object references to make these loops faster
		# Loop through each tile and set its batch attribute to the given batch if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('batch', batch), row), self.tiles)

	def set_group(self, group):
		# TODO There should be a list of actual tile object references to make these loops faster
		# Loop through each tile and set its group attribute to the given group if it is not None
		map(lambda row: map(lambda tile: tile and tile.__setattr__('group', group), row), self.tiles)

	# TODO Ideally we shouldn't need this class to know how to reload itself, the reloader alone should handle that
	def reload(self, level_data):
		self.create_tile_map(level_data)
