from game.animation import TiledAnimation
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.animation.TiledAnimation`."""
	return graphics_type == 'tiled animation'

def factory(*args, **kwargs):
	"""Returns a :class:`game.animation.TiledAnimation` for the given arguments."""
	return TiledAnimation.from_image(*args, **kwargs)

install_graphics_module(__name__)
