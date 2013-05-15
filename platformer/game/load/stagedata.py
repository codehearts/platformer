import json
from ..settings import demo_settings

class StageData():

	def __init__(self, level = 0):
		# TODO fix this path
		stage_file = open('/home/nate/Dropbox/platformer/platformer/game/stages/demo.json')

		# @TODO We're pretending this data came from a JSON file
		self.tile_data = demo_settings.TILE_DATA

		self.map = json.load(stage_file)

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
	def get_tile_data(self):
		return self.tile_data

	# Returns an array map of the stage
	def get_map(self):
		return self.map

	# Returns an array of stage events for this level
	def get_stage_events(self):
		return self.tile_data['events']

	# Returns information about where to initiate the player
	def get_player_data(self):
		return self.player_data

	# Returns information about where to initiate non-playable characters
	def get_character_data(self):
		return self.character_data

	def reload(self, level=0):
		# TODO fix this path
		stage_file = open('/home/nate/Dropbox/platformer/platformer/game/stages/demo.json')

		# @TODO We're pretending this data came from a JSON file
		self.tile_data = demo_settings.TILE_DATA

		self.map[:] = json.load(stage_file)

		stage_file.close()
