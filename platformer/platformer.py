import pyglet
from pyglet.window import key
from game import load, camera, backgrounds, stageevents, reloader
from game.settings import general_settings

# Graphical output window
game_window = pyglet.window.Window(800, 600, caption='Platformer Demo')
#game_window.set_icon(pyglet.resource.image('icon.png')) @TODO Load an icon

# Handler for all keyboard events
key_handler = key.KeyStateHandler()

# TODO The stage to load shouldn't be passed like this, there should be some sort of saved data handler that passes this
# TODO Stage data should be loaded by the stage loader
level_data = load.LevelData('demo') # TODO Could this be a Level class which contains Stage and LevelEvents objects?

stage = load.Stage(level_data)

#characters = load.Characters(stage_data.get_character_data(), stage.get_tiles())

# TODO Should probably just pass the reference to the stage here
player = load.Player(level_data.get_player_data(), stage.get_tiles(), key_handler)
game_window.push_handlers(player.character.key_handler)

cam = camera.Camera(player.character, game_window, stage.get_tiles())
cam.focus() # TODO Should this be called on init?

# TODO I should not have to pass level_data just so this can pass the level title to an Overlay object
background = backgrounds.Layers(level_data, cam)

stage_events = stageevents.StageEvents(player.character, cam, level_data.get_stage_events())

module_reloader = reloader.Reloader(stage, player, game_window, cam, background, stage_events, key_handler)

@game_window.event
def on_draw():
	game_window.clear()

	background.draw_background()
	stage.draw()
	#characters.draw()
	player.draw()
	background.draw_foreground()

def update(dt):
	player.update(dt)

	stage_events.update()

	cam.update(dt)
	background.update(dt)

	module_reloader.update()

	# @TODO characters.update() method
	"""for character in characters.get_characters():
		character.update(dt)"""

if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, general_settings.FRAME_LENGTH)

	pyglet.app.run()
