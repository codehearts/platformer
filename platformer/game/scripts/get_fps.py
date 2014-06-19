from pyglet.clock import get_fps as pyglet_get_fps

def get_fps():
	"""Returns the current frame rate as an integer in a string."""
	return str(int(pyglet_get_fps()))
