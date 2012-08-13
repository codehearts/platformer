from pyglet.window import key
from game import load

class Reloader(object):
	
	def __init__(self):
		self.key_handler = key.KeyStateHandler()
	
	def update(self, stage_data, level, level_tiles, player, game_window, cam, background, stage_events):
		# If R is pressed, reload the game modules
		if self.key_handler[key.R]:
			reload(load)
			print 'reloading'
			stage_data = load.StageData(0)

			level = load.Stage(stage_data.get_tile_data(), stage_data.get_map())
			level_tiles = level.get_tiles()

			#characters = load.Characters(stage_data.get_character_data(), level_tiles)

			#player = load.Player(stage_data.get_player_data(), level_tiles)
			#game_window.push_handlers(player.character.key_handler)

			#cam = camera.Camera(player.character, game_window, level_tiles)
			#cam.focus()

			background = backgrounds.Backgrounds(stage_data.get_tile_data(), cam)

			stage_events = stageevents.StageEvents(player.character, cam, stage_data.get_stage_events())