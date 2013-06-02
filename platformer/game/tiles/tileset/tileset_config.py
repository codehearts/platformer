from json import loads as parse_json

class TilesetConfig(object):
	"""Tileset config data which defines how each tile in a tileset should behave.

	Tileset config files should be JSON, where each key is a tile value
	from the tileset and each value is an object specifying additional
	parameters to pass when creating the tile object.

	If a tile value is not present in the config file, no additional
	parameters will be set upon tile creation.

	Tileset config files should be located in the same directory as
	their associated tileset image. This should be ``{resources_dir}/{tilesets_dir}/{tileset_name}/config.json``.
	"""

	def __init__(self, config_data=None):
		"""Parses the tileset config string for a tileset.

		Kwargs:
			config_data (str): A JSON formatted string of config data for this tileset.

		Raises:
			ValueError: The config file is not formatted as valid JSON.
		"""
		self._config = {}

		if config_data:
			self._parse_config(config_data)

	def _parse_config(self, config_data):
		"""Parses a tileset config string.

		Args:
			config_data (str): A JSON formatted string of config data for this tileset.

		Raises:
			ValueError: The config file is not formatted as valid JSON.
		"""
		# Attempt to parse the config data
		raw_config = parse_json(config_data)

		# Convert the keys from str to int (the keys are tile values)
		for tile_value, tile_config in raw_config.iteritems():
			self._config[int(tile_value)] = tile_config

	def get_tile_entry(self, tile_value):
		"""Returns the tileset config entry for the given tile value.

		Args:
			tile_value (int): The integer value of a tile in the tileset.

		Returns:
			A dict of additional parameters for creating a new tile object.
			If there are no additional parameters, an empty dict is returned.
		"""
		# If the value has an entry in the config, return the config entry
		if tile_value in self._config:
			return self._config[tile_value]

		# Otherwise return an empty entry
		return {}
