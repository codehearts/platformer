from pyglet.resource import image as open_resource_image
from pyglet.sprite import Sprite
from sys import modules
import glob
import os

def install_graphics_module(module_name):
	"""Installs the specified module to be used for graphical output.

	Args:
		module_name (string): The name of the module to install.
	"""
	global installed_graphics

	graphics_module = modules[module_name]
	installed_graphics.append({
		'recognizer': getattr(graphics_module, 'recognizer'),
		'factory': getattr(graphics_module, 'factory'),
	})



def _sprite_factory(*args, **kwargs):
	"""Returns a :class:`pyglet.sprite.Sprite` for the given arguments."""
	return Sprite(img=open_resource_image(kwargs['graphic']), *args)

installed_graphics = [
	# Pre-install Pyglet's Sprite module
	{
		'recognizer': lambda graphics_type: graphics_type == 'image',
		'factory': _sprite_factory,
	}
]

# Get all files not beginning with an underscore and import them
_import_modules = glob.glob(os.path.dirname(__file__) + '/*.py')
__all__ = [os.path.basename(f)[:-3] for f in _import_modules if not os.path.basename(f).startswith('_')]
from . import *
