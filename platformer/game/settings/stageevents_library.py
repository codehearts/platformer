from pyglet import clock
from game.easing import EaseIn, EaseOut

# TODO Look into using pyglet's EventDispatcher
def demo_stage_1(modules):
    modules['player'].disable()
    modules['camera'].focus_on_tile(45.5, 3, 1, easing=EaseOut)

    clock.schedule_once(demo_stage_1_end, 1.5, modules)

def demo_stage_1_end(delay_time, modules):
    modules['player'].enable()
    modules['camera'].focus_on_target(1, easing=EaseIn)
