from pyglet.clock import get_fps as pyglet_get_fps

def get_fps():
    return str(int(pyglet_get_fps()))
