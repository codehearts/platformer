from tile import Tile
from custom_tile_loader import custom_tile_types

def create_tile(*args, **kwargs):
	"""Creates the appropriate tile object for the given tile arguments.

	Kwargs:
		type (str): The type of tile that is expected.

	Returns:
		A tile object.
	"""
	tile_type = kwargs.pop('type', None)

	# If a factory method has been provided for this tile type, use it
	if tile_type in custom_tile_types:
		return custom_tile_types[tile_type](*args, **kwargs)

	return Tile(*args, **kwargs)
