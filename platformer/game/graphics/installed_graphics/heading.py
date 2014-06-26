from game.text import Heading
from . import install_graphics_module

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.text.heading.Heading`."""
	return graphics_type == 'heading'

def factory(*args, **kwargs):
	"""Returns a :class:`game.text.heading.Heading` for the given arguments."""
	return Heading(*args, **kwargs)

install_graphics_module(__name__)
