import pyglet
from pyglet.window import key
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from game import load, camera, stageevents, reloader
from game.layers import layer_manager, fixed_layer, fixed_animation_layer, fixed_text_layer, texture_tile_map_layer, physical_object_layer
from game.settings import general_settings
from game.animation import tiled_animation
from game.text import heading, live_text
from game.easing.ease_out import EaseOut
from game.tiles import texture_tile_map
from game.tiles import tileset

# Graphical output window
game_window = pyglet.window.Window(800, 600, caption='Platformer Demo')
#game_window.set_icon(pyglet.resource.image('icon.png')) @TODO Load an icon

# Handler for all keyboard events
key_handler = key.KeyStateHandler()

# TODO The stage to load shouldn't be passed like this, there should be some sort of saved data handler that passes this
# TODO Stage data should be loaded by the stage loader
level_data = load.LevelData('demo') # TODO Could this be a Level class which contains Stage and LevelEvents objects?

# TODO Stage should not take in so much data
#stage = tile_map.TileMap(level_data.get_stage_map(), level_data.get_tile_sprite_file(), rows=level_data.get_stage_size()[0], cols=level_data.get_stage_size()[1])
stage_tileset = tileset.Tileset.load('demo', rows=level_data.get_stage_size()[0], cols=level_data.get_stage_size()[1])
stage = texture_tile_map.TextureTileMap(level_data.get_stage_map(), stage_tileset)

#characters = load.Characters(stage_data.get_character_data(), stage.get_tiles())

# TODO Should probably just pass the reference to the stage here
player = load.Player(level_data.get_player_data(), stage.get_tiles(), key_handler)
game_window.push_handlers(player.character.key_handler)

cam = camera.Camera(player.character, game_window, stage.get_tiles())
cam.focus() # TODO Should this be called on init?

player_layer = physical_object_layer.PhysicalObjectLayer(player.character, cam)

# TODO Layer creation should be handled dynamically by the level loader. I'm creating these manually until I implement that ability
background = fixed_layer.FixedLayer(pyglet.sprite.Sprite(img=pyglet.resource.image(level_data.get_background_image_file())), cam)
stage_layer = texture_tile_map_layer.TextureTileMapLayer(stage, cam)
#stage_layer = tile_map_layer.TileMapLayer(stage, cam)
transition_animation = tiled_animation.TiledAnimation.from_image(
			pyglet.resource.image('transition.png'),
			1,
			31,
			EaseOut.get_frame_durations(1*31, 1.25, ease_power=0.5),
			cam.width,
			cam.height,
			delay=0.5
		)
transition_layer = fixed_animation_layer.FixedAnimationLayer(transition_animation, cam, on_animation_end=lambda animation, layer: layer.delete())
title_layer = fixed_text_layer.FixedTextLayer(heading.Heading(text=level_data.get_level_title(), font_size=18, anchor_x='center', anchor_y='center'), cam, offset_x=cam.half_width, offset_y=cam.half_height, duration=2.25)
fps_text = live_text.LiveText(lambda: str(int(pyglet.clock.get_fps())))
fps_text.set_style('background_color', (0,0,0,255))
fps_layer = fixed_text_layer.FixedTextLayer(fps_text, cam, offset_x=10, offset_y=10)
dash_text = live_text.LiveText(lambda: str(int((player.character.max_dash_time - player.character.time_dashed) / player.character.max_dash_time * 100)))
dash_text.set_style('background_color', (0,0,0,255))
dash_layer = fixed_text_layer.FixedTextLayer(dash_text, cam, offset_x=40, offset_y=10)
layers = layer_manager.LayerManager([background, stage_layer, player_layer, dash_layer, transition_layer, title_layer, fps_layer])

# TODO This should be a LevelEvents object inside a Level class
stage_events = stageevents.StageEvents(player.character, cam, level_data.get_stage_events())

module_reloader = reloader.Reloader(stage, player, game_window, cam, background, stage_events, key_handler)

@game_window.event
def on_draw():
	# TODO It's possible that this could be removed if it's a significant performance bottleneck
	game_window.clear()

	#characters.draw()
	layers.draw()

def update(dt):
	# TODO Write a manager to handle updates and update order?
	player.update(dt)
	stage_events.update()

	cam.update(dt)
	layers.update(dt)

	module_reloader.update()

	# @TODO characters.update() method
	"""for character in characters.get_characters():
		character.update(dt)"""

if __name__ == '__main__':
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	pyglet.clock.schedule_interval(update, general_settings.FRAME_LENGTH)
	pyglet.app.run()
