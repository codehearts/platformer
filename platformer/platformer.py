import pyglet
from pyglet.window import key
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from game import load, viewport, stageevents
from game import layers
from game.settings import general_settings
from game.animation import tiled_animation
from game.text import heading, live_text
from game.easing import EaseOut
from game.bounded_box import BoundedBox
from game import tiles
from game.settings.general_settings import TILE_SIZE

# Graphical output window
# TODO Better caption
game_window = pyglet.window.Window(800, 600, caption='Platformer Demo')
#game_window.set_icon(pyglet.resource.image('icon.png')) @TODO Load an icon

# Handler for all keyboard events
key_handler = key.KeyStateHandler()

# TODO The stage to load shouldn't be passed like this, there should be some sort of saved data handler that passes this
# TODO Stage data should be loaded by the stage loader
level_data = load.LevelData('demo') # TODO Could this be a Level class which contains Stage and LevelEvents objects?

# TODO There should be a HUD class and loader which can handle commonly reused HUD objects
# TODO Maybe this should just be done in Python (a better idea might be to write custom python code in a separate file from the level config)
sample_level_data = {
	'title': 'Demo Stage',
	'tilesets': ['demo'],
	'layers': {
		'background': {
			'type': 'image',
			'graphic': 'sky.png',
			'fixed': True,
			'static': True
		},
		'stage': {
			'type': 'tile map',
			'tileset': 'demo'
                        # TODO Each layer should have its own function to turn a string into the appropriate graphics object
		},
		'player': {
			'type': 'player'
		},
		'dash': {
			'type': 'live text',
			'graphic': 'get_player_dash_percentage',
			'offset_x': 40,
			'offset_y': 10,
			'fixed': True
		},
		# TODO Need a way to group common layers like this
                # TODO Could use an underscore for reserved layer names, such as a special "_group" layer containing sublayers
		'transition': {
			'type': 'tiled animation',
			'graphic': 'transition.png',
			# TODO Need a better way to specify graphics like this
			'fixed': True
		},
		'title': {
			'type': 'heading',
			'graphic': 'Demo Stage', # TODO Should be able to get this from the level config
			# TODO Can't be centered by this config
		}
	},
        'scripts': {
            'level_demo',
            'dash_meter',
            'fps',
        },
}

stage_tileset = tiles.Tileset.load('demo')
stage = tiles.TextureTileMap(level_data.get_stage_map(), stage_tileset)

#characters = load.Characters(stage_data.get_character_data(), stage.get_tiles())

# TODO Should probably just pass the reference to the stage here
player = load.Player(level_data.get_player_data(), stage.tiles, key_handler)
game_window.push_handlers(player.character.key_handler)

stage_boundary = BoundedBox(0, 0, stage.cols*TILE_SIZE, stage.rows*TILE_SIZE)
cam = viewport.Camera(0, 0, 800, 600, bounds=stage_boundary, target=player.character)
cam.focus() # TODO Should this be called on init?

player_layer = layers.create_from(player.character)

# TODO Layer creation should be handled dynamically by the level loader. I'm creating these manually until I implement that ability
background = layers.create_from(pyglet.sprite.Sprite(img=pyglet.resource.image(level_data.get_background_image_file())), fixed=True, static=True)
#stage_layer = layers.TextureTileMapLayer(stage, cam)
stage_layer = layers.create_from(stage)
#stage_layer = tile_map_layer.TileMapLayer(stage, cam)
transition_animation = tiled_animation.TiledAnimation.from_image(
			pyglet.resource.image('transition.png'),
			1,
			31,
			EaseOut.get_frame_durations(1*31, 1.25, ease_power=0.75),
			cam.width,
			cam.height,
			delay=0.5
		)
transition_layer = layers.create_from(transition_animation, on_animation_end=lambda animation, layer: layer.delete(), fixed=True)
title_layer = layers.create_from(heading.Heading(text=level_data.get_level_title(), font_size=18, anchor_x='center', anchor_y='center'), offset_x=cam.half_width, offset_y=cam.half_height, duration=2.25, fixed=True, static=True)
fps_text = live_text.LiveText(lambda: str(int(pyglet.clock.get_fps())))
fps_text.set_style('background_color', (0,0,0,255))
fps_layer = layers.create_from(fps_text, offset_x=10, offset_y=10, fixed=True)
dash_text = live_text.LiveText(lambda: str(int((player.character.max_dash_time - player.character.time_dashed) / player.character.max_dash_time * 100)))
dash_text.set_style('background_color', (0,0,0,255))
dash_layer = layers.create_from(dash_text, offset_x=40, offset_y=10, fixed=True)
layer_manager = layers.LayerManager(cam, [background, stage_layer, player_layer, dash_layer, transition_layer, title_layer, fps_layer])

# TODO This should be a LevelEvents object inside a Level class
stage_events = stageevents.StageEvents(player.character, cam, level_data.get_stage_events())

# TODO Make this work again
#module_reloader = reloader.Reloader(stage, player, game_window, cam, background, stage_events, key_handler)

@game_window.event
def on_draw():
	# TODO It's possible that this could be removed if it's a significant performance bottleneck
	game_window.clear()

	#characters.draw()
	layer_manager.draw()

def update(dt):
	# TODO Write a manager to handle updates and update order?
	#player.update(dt)
	stage_events.update()

	#cam.update(dt)
	layer_manager.update(dt)

	#module_reloader.update()

	# @TODO characters.update() method
	"""for character in characters.get_characters():
		character.update(dt)"""

if __name__ == '__main__':
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	pyglet.clock.schedule_interval(update, general_settings.FRAME_LENGTH)
	pyglet.app.run()
