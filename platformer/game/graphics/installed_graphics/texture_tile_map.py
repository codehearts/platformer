from game.tiles import TextureTileMap
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.tiles.TextureTileMap`."""
	return graphics_type == 'tile map'

def factory(*args, **kwargs):
	"""Returns a :class:`game.tiles.TextureTileMap` for the given arguments."""
	return TextureTileMap(*args, **kwargs)

install_graphics_module(__name__)
