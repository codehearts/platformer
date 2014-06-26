from game.viewport import Camera
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`viewport.Camera`."""
	return graphics_type == 'camera'

def factory(*args, **kwargs):
	"""Returns a :class:`viewport.Camera` for the given arguments."""
	return Camera(*args, **kwargs)

install_graphics_module(__name__)
