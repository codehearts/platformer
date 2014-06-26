from game.load import Player
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.physical_objects.Player`."""
	return graphics_type == 'player'

def factory(*args, **kwargs):
	"""Returns a :class:`game.physical_objects.Player` for the given arguments."""
	return Player(*args, **kwargs)

install_graphics_module(__name__)
