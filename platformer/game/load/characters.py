import pyglet
from game import bestiary, util

class Characters():

	def __init__(self, character_data, stage):
		self.batch = pyglet.graphics.Batch()
		self.characters = []

		# Create a list of all character data
		for name, tile in character_data.items():
		   self.characters.append(single_character(name, tile['x'], tile['y'], stage, self.batch))

	# Returns a list of all characters
	def get_characters(self):
		return self.characters

	# Draw all characters to the screen
	def draw(self):
		self.batch.draw()



# Loads a single character based on their bestiary name, tile coordinates, and graphics batch
# TODO tile_x and tile_y should be kwargs
def single_character(name, tile_x, tile_y, stage, batch=None):
	# Get our character data from the bestiary
	character_data = bestiary.look_up[name].copy()
	character_class = character_data['class']

	# Remove the class from the list of arguments we'll be passing to its constructor
	del character_data['class']

	# Convert tile location to coordinates
	coordinates = util.tile_to_coordinate(tile_x, tile_y)
	character_data['x'], character_data['y'] = coordinates[0], coordinates[1]

	return character_class(batch=batch, stage=stage, **character_data)
