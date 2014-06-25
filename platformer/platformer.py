import pyglet
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from game import viewport, stageevents
from game import layers
from game.settings import general_settings
from game.animation import tiled_animation
from game.text import heading, live_text
from game.easing import EaseOut
from game.bounded_box import BoundedBox
from game import tiles
from game.settings.general_settings import TILE_SIZE
from game.load import Level
import game

# Graphical output window
# TODO Better caption
game_window = pyglet.window.Window(800, 600, caption='Platformer Demo')
#game_window.set_icon(pyglet.resource.image('icon.png')) @TODO Load an icon

# TODO There should be a HUD class and loader which can handle commonly reused HUD objects
# TODO Need a way to group common layers like the transition and title layer (Could use an underscore for reserved layer names, such as a special "_group" layer containing sublayers)
# TODO Allow the config files access to simple values like the window size so things like centering are possible and the level title can be reused instead of hardcoding it everywhere it's needed

# TODO Allow for setting the background color of these layers' graphics
#fps_text.set_style('background_color', (0,0,0,255))
#dash_text.set_style('background_color', (0,0,0,255))

#characters = load.Characters(stage_data.get_character_data(), stage.get_tiles())

game_window.push_handlers(game.key_handler)

# TODO The stage to load shouldn't be passed like this, there should be some sort of saved data handler that passes the level to load
level = Level.load('demo')
game.level = level # Make it globally available

# TODO This should be a LevelEvents object inside a Level class
events = {
    'player_events': [
        {
            'run': 'once',
            'condition': lambda player: player.x_tile >= 25,
            'function': 'demo_stage_1'
        }
    ]
}
# TODO level.layers[2] is a temporary way of getting the player layer
stage_events = stageevents.StageEvents(level.layer_manager.layers['player'].graphic, level.camera, events)

# TODO Make this work again
#module_reloader = reloader.Reloader(stage, player, game_window, cam, background, stage_events, key_handler)

@game_window.event
def on_draw():
	# TODO It's possible that this could be removed if it's a significant performance bottleneck
	game_window.clear()

	level.layer_manager.draw()

def update(dt):
	stage_events.update()

        # TODO The level object should have its own update method
	level.layer_manager.update(dt)

	#module_reloader.update()

if __name__ == '__main__':
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	pyglet.clock.schedule_interval(update, general_settings.FRAME_LENGTH)
	pyglet.app.run()
