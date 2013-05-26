from pyglet import clock
from game.settings import general_settings

# TODO Look into using pyglet's EventDispatcher
def demo_stage_1(modules):
    modules['player'].disable()
    modules['camera'].move_to_tile(45.5, 3, 1, general_settings.EASE_OUT)

    clock.schedule_once(demo_stage_1_end, 1.5, modules)

def demo_stage_1_end(delay_time, modules):
    modules['player'].enable()
    modules['camera'].focus_on_target(0.4)
