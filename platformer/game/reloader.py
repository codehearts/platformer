from pyglet.window import key
from game import load, stageevents, backgrounds

class Reloader(object):

	def __init__(self, stage_data, level, level_tiles, player, game_window, cam, background, stage_events, key_handler):
		self.stage_data = stage_data
		self.level = level
		self.level_tiles = level_tiles
		self.player = player
		self.game_window = game_window
		self.cam = cam
		self.background = background
		self.stage_events = stage_events
		self.key_handler = key_handler

		# True if the engine is currently being reloaded
		self.is_reloading = False

	def update(self):
		# If R is pressed, reload the game modules
		if self.key_handler[key.R] and not self.is_reloading:
			# Lock the reloader
			self.is_reloading = True
			print 'reloading'
			reload(load)

			self.stage_data.reload(0)

			old = self.level.get_tiles()
			print id(self.level.get_tiles())
			self.level.reload(self.stage_data.get_tile_data(), self.stage_data.get_map())
			print id(self.level.get_tiles())
			print old == self.level.get_tiles()
			self.level_tiles[:] = self.level.get_tiles()

			#characters = load.Characters(stage_data.get_character_data(), level_tiles)

			#player = load.Player(stage_data.get_player_data(), level_tiles)
			#game_window.push_handlers(player.character.key_handler)

			#cam = camera.Camera(player.character, game_window, level_tiles)
			#cam.focus()

			self.background.__dict__.update(backgrounds.Backgrounds(self.stage_data.get_tile_data(), self.cam).__dict__)

			#self.stage_events.__dict__.update(stageevents.StageEvents(self.player.character, self.cam, self.stage_data.get_stage_events()).__dict__)

			# Unlock the reloader
			self.is_reloading = False
