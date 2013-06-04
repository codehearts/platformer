import unittest
from game.tiles.tileset import TilesetConfig
from ..util.tileset import get_valid_config_data

class TestTilesetConfig(unittest.TestCase):
	"""Tests parsing of tileset config data."""

	def setUp(self):
		self.JSON_config = None
		self.expected_config = None

		self.tileset_config = None



	def test_valid_tileset_config(self):
		"""Tests parsing valid tileset configs with TilesetConfig."""
		# Initialize valid test config data
		self.setup_valid_config_data()

		# Test creating a config object for the test data
		self.tileset_config = TilesetConfig(self.JSON_config)

		self.assert_tileset_config("Passed valid JSON string.")

	def test_invalid_tileset_config(self):
		"""Tests parsing invalid tileset configs with TilesetConfig."""
		# Initialize invalid test config data
		self.setup_invalid_config_data()

		# Attempt to Create a config object for the test data
		try:
			self.assertRaises(ValueError, TilesetConfig, self.JSON_config)
		except:
			raise AssertionError("Tileset did not raise ValueError when passed invalid JSON.")

	def test_empty_tileset_config(self):
		"""Tests parsing empty tileset configs with TilesetConfig."""
		# Ensure nothing is raised when initializing an empty config
		self.tileset_config = TilesetConfig('')



	# Helper methods

	def assert_tileset_config(self, condition=''):
		"""Asserts that the tileset config entries are correct."""
		if condition:
			condition = ' Condition: '+condition

		for tile_value, expected_tile_entry in self.expected_config.iteritems():
			self.assertEqual(self.tileset_config.get_tile_entry(tile_value), expected_tile_entry, "Tile's config entry is incorrect." + condition)



	def setup_valid_config_data(self):
		"""Sets up valid JSON test config data.

		This config makes use of custom tile types, string values,
		integer values, and boolean values.
		"""
		config = get_valid_config_data()

		# Valid JSON config for testing
		self.JSON_config = config['JSON']

		# Expected values for the parsed tileset config
		self.expected_config = config['expected']

	def setup_invalid_config_data(self):
		"""Sets up invalid JSON test config data.

		This config will cause the JSON parser to raise a ValueError.
		"""
		# Invalid JSON config for testing
		self.JSON_config = '''
			"1": {
				"type": "custom",
				"faces": "right",
			}
			"3": {
				"type": "custom2",
			}
			"5": {
				"x": 32,
				"y": 128,
			}
			"7": {
				"is_collidable": false,
			}'''
