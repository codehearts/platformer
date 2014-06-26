from game.tiles import Tileset
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.tiles.tileset.Tileset`."""
	return graphics_type == 'tileset'

def factory(*args, **kwargs):
	"""Returns a :class:`game.tiles.tileset.Tileset` for the given arguments."""
	return Tileset.load(*args, **kwargs)

install_graphics_module(__name__)
