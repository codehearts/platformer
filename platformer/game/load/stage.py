import pyglet
from game import tile, util
from stagedata import StageData
from ..settings import tile_settings

# TODO Clean up stage.data methods to feel more intuitive

class Stage():

	def __init__(self, stage_name):
		self.data = StageData(stage_name)

		self.batch = pyglet.graphics.Batch()
		self.tile_data = self.data.tile_data
		self.tiles = [] # Map of all tile objects
		self.tile_map = [] # Map of all numeric tile values

		self.load_tiles(self.data.stage_map)

	# Load the tile map into an array of tiles indexed with an anchor point at the bottom left
	def load_tiles(self, stage_map):
		self.tiles[:] = [[None] * len(stage_map[0]) for i in xrange(len(stage_map))] # Initiate an empty stage
		self.tile_map[:] = [[0] * len(stage_map[0]) for i in xrange(len(stage_map))] # Initiate an empty stage

		tile_image = pyglet.resource.image(self.tile_data['file'])
		tileset = pyglet.image.TextureGrid(pyglet.image.ImageGrid(tile_image, self.tile_data['size'][0], self.tile_data['size'][1]))
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
					row = ((tile_value-1) / self.tile_data['size'][1])
					col = tile_value - row * self.tile_data['size'][1] - 1
					row = self.tile_data['size'][0] - row - 1 # Adjust for index 0 being at the bottom left

					# Determine whether this is a special tile
					tile_type = tile_settings.NORMAL
					for tile_key, special_values in self.tile_data['key'].iteritems():
						if tile_value in special_values:
							tile_type = tile_key

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

	# TODO Ideally we shouldn't need this class to know how to reload itself, the reloader alone should handle that
	def reload(self, stage_name):
		self.data.reload(stage_name)

		self.tile_data = self.data.tile_data
		self.load_tiles(self.data.stage_map)
