import json
from pyglet.resource import file as open_resource_file
from ..settings import demo_settings

# Loads data for the specified level
# This can include player positioning, stage events, etc.
class LevelData(object):

	def __init__(self, stage_name):
		stage_file = open_resource_file('stages/'+stage_name+'.json')

		# TODO Move this data to the JSON file
		self.level_data = demo_settings.TILE_DATA
		self.level_data['stage_map'] = json.load(stage_file)

		stage_file.close()

		self.player_data = {
			'x': 25,
			'y': 16
		}

		self.character_data = {
			'test_object_6': {
				'x': 40,
				'y': 7.5
			}
		}

	# Returns metadata about the stage tiles
	def get_level_data(self):
		return self.level_data

	# Returns an array map of the stage
	def get_stage_map(self):
		return self.level_data['stage_map']

	# Returns a tuple of the dimensions of the stage
	def get_stage_size(self):
		return self.level_data['size']

	# Returns the title of the level
	def get_level_title(self):
		return self.level_data['name']

	# TODO Group all tile stuff together, group all stage stuff together
	# Returns a dictionary with assignments of tile types (slopes, etc.) to numeric tile values
	def get_tile_type_assignments(self):
		return self.level_data['key']

	# Returns an array of stage events for this level
	def get_stage_events(self):
		return self.level_data['events']

	# Returns information about where to initiate the player
	def get_player_data(self):
		return self.player_data

	# Returns information about where to initiate non-playable characters
	def get_character_data(self):
		return self.character_data

	# Returns the location of the background image file
	def get_background_image_file(self):
		return self.level_data['background']

	# Returns the location of the tile sprite image file
	def get_tile_sprite_file(self):
		return self.level_data['file']

	# TODO Ideally we shouldn't need this class to bother with reloading itself
	def reload(self, stage_name):
		stage_file = open_resource_file('stages/'+stage_name+'.json')

		# @TODO We're pretending this data came from a JSON file
		self.level_data = demo_settings.TILE_DATA

		self.level_data['stage_map'][:] = json.load(stage_file)

		stage_file.close()
