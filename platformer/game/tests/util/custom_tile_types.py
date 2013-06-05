from game.tiles.custom_tile_loader import custom_tile_types
from game.tiles.tile import Tile

"""Provides custom tile types for testing with.

A 'custom' tile type can be registered which is subclassed by four class:
``UpFacingTile``, ``DownFacingTile``, ``LeftFacingTile``, and
``RightFacingTile``. The appropriate tile object is returned via
the factory method ``custom_tile_factory``, which accepts an optional
``faces`` argument specifying which direction the created tile
object should face. The factory default is ``UpFacingTile`` if ``faces``
is invalid or not set.

A 'custom2' tile type can be registered. This type has no factory method
and merely uses its class object as its factory callback.

``setUp`` and ``tearDown`` should be called during the setup and teardown
of tests to establish a fresh custom tile environment and then restore it
to its original condition when the tests are finished.

To register each custom tile type for use with the tile factory,
``register_{type_name}`` should be called. ``register_all`` can be called
to register all custom tile types at once.
"""

# Saved reference to the original custom tile type callbacks
_saved_custom_tile_types = None

def setUp():
	"""Saves and removes all set custom tile type callbacks.

	``tearDown()`` should be called when these custom testing types are
	no longer needed to restore the custom tile type callbacks to its
	original state.
	"""
	global _saved_custom_tile_types, custom_tile_types

	_saved_custom_tile_types = custom_tile_types.copy()
	custom_tile_types.update({})

def tearDown():
	"""Restores the custom tile type callbacks."""
	global _saved_custom_tile_types, custom_tile_types

	# tearDown can be called before setUp
	if _saved_custom_tile_types is not None:
		custom_tile_types.update(_saved_custom_tile_types)

def register_custom():
	"""Registers a factory callback for the 'custom' tile type."""
	custom_tile_types['custom'] = custom_tile_factory

def register_custom2():
	"""Registers a class callback for the 'custom2' tile type."""
	custom_tile_types['custom2'] = Custom2Tile

def register_all():
	"""Registers callbacks for all custom tile types."""
	register_custom()
	register_custom2()



# Custom Tile subclasses

class _CustomTile(Tile):
	"""Custom tile subclass."""

	type = 'custom'
	faces = None # Direction the tile faces

class UpFacingTile(_CustomTile):
	faces = 'up'

class DownFacingTile(_CustomTile):
	faces = 'down'

class LeftFacingTile(_CustomTile):
	faces = 'left'

class RightFacingTile(_CustomTile):
	faces = 'right'



class Custom2Tile(Tile):
	"""Second custom tile subclass.

	This class has no special factory method for itself.
	"""

	type = 'custom2'



# Custom tile type factory methods

def custom_tile_factory(*args, **kwargs):
	"""Creates a 'custom' tile object facing the specified direction.

	If a direction is not specified or is invalid, an UpFacingTile is created.

	Kwargs:
		faces (str): The direction the created tile should face.

	Returns:
		A tile object facing the specified direction.
	"""
	faces = kwargs.pop('faces', None)
	tiles = [UpFacingTile, DownFacingTile, LeftFacingTile, RightFacingTile]

	for tile_class in tiles:
		if tile_class.faces == faces:
			return tile_class(*args, **kwargs)

	return UpFacingTile(*args, **kwargs)
