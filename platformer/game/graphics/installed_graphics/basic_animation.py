from game.animation import BasicAnimation
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.animation.BasicAnimation`."""
	return graphics_type == 'animation'

def factory(*args, **kwargs):
	"""Returns a :class:`game.animation.BasicAnimation` for the given arguments."""
	return BasicAnimation(*args, **kwargs)

install_graphics_module(__name__)
