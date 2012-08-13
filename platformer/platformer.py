import pyglet
from game import load, camera, backgrounds, stageevents, reloader
from game.settings import general_settings

game_window = pyglet.window.Window(800, 600, caption='Platformer Demo')
#game_window.set_icon(pyglet.resource.image('icon.png')) @TODO Load an icon

# @TODO The reloader shouldn't have to duplicate this code

stage_data = load.StageData(0)

level = load.Stage(stage_data.get_tile_data(), stage_data.get_map())
level_tiles = level.get_tiles()

#characters = load.Characters(stage_data.get_character_data(), level_tiles)

player = load.Player(stage_data.get_player_data(), level_tiles)
game_window.push_handlers(player.character.key_handler)

cam = camera.Camera(player.character, game_window, level_tiles)
cam.focus()

background = backgrounds.Backgrounds(stage_data.get_tile_data(), cam)

stage_events = stageevents.StageEvents(player.character, cam, stage_data.get_stage_events())

module_reloader = reloader.Reloader()

@game_window.event
def on_draw():
	game_window.clear()
	
	background.draw_background()
	level.draw()
	#characters.draw()
	player.draw()
	background.draw_foreground()

def update(dt):
	player.update(dt)
	
	stage_events.update()
	
	cam.update(dt)
	background.update(dt)
	
	module_reloader.update(stage_data, level, level_tiles, player, game_window, cam, background, stage_events)
	
	# @TODO characters.update() method
	"""for character in characters.get_characters():
		character.update(dt)"""

if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, general_settings.FRAME_LENGTH)
	
	pyglet.app.run()