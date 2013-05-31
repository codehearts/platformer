from pyglet.window import key
# TODO Uncomment the bottom when stageevent reloading is implemented
#from game import load, stageevents, backgrounds
from game import load

# TODO Make this class work again
class Reloader(object):

	# TODO Ideally this class would not need to know about all these objects, it would have a dynamic collection of objects that get reloaded or something
	def __init__(self, stage, player, game_window, cam, background, stage_events, key_handler):
		self.stage = stage
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
			reload(load)

			level_data = load.LevelData('demo')

			# Reload the level and stage tiles
			# TODO Instead of reloading this way, a new object should be created, its properties copied, and then the reference to the "new" object destroyed
			self.stage.reload(level_data)
			#self.level_tiles[:] = self.level.get_tiles()

			#characters = load.Characters(stage_data.get_character_data(), level_tiles)

			#player = load.Player(stage_data.get_player_data(), level_tiles)
			#game_window.push_handlers(player.character.key_handler)

			#cam = camera.Camera(player.character, game_window, level_tiles)
			#cam.focus()

			#self.background.__dict__.update(backgrounds.Backgrounds(level_data, self.cam).__dict__)

			#self.stage_events.__dict__.update(stageevents.StageEvents(self.player.character, self.cam, self.stage_data.get_stage_events()).__dict__)

			# Unlock the reloader
			self.is_reloading = False
