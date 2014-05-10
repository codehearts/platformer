from game.easing import EaseOut
from pyglet.resource import image

transition_image = image("transition.png")
transition_durations = EaseOut.get_frame_durations(1*31, 1.25, ease_power=0.75)
