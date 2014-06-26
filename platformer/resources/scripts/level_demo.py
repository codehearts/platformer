from game.easing import EaseOut
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE
from pyglet.resource import image

transition_image = image('transition.png')
transition_durations = EaseOut.get_frame_durations(1*31, 1.25, ease_power=0.75)
bounds = BoundedBox(0, 0, 1000*TILE_SIZE, 1000*TILE_SIZE)
