import pyglet.resource
from game.settings import general_settings

_saved_paths = {}

def setUp():
	"""Saves the current resource paths and changes them to point to
	the testing resource directories.

	``tearDown()`` should be called when tests requiring file
	resources are completed to restore the resource paths to
	their original state.
	"""
	global _saved_paths

	_saved_paths['path'] = pyglet.resource.path
	_saved_paths['tilesets'] = general_settings.TILESET_DIRECTORY

	pyglet.resource.path = ['game/tests/resources']
	general_settings.TILESET_DIRECTORY = 'tilesets'
	pyglet.resource.reindex()

def tearDown():
	"""Restores the resource paths to their original states."""
	global _saved_paths

	# tearDown may be called before setUp
	if 'resources' in _saved_paths:
		pyglet.resource.path = _saved_paths['resource']
		general_settings.TILESET_DIRECTORY = _saved_paths['tilesets']
		pyglet.resource.reindex()
