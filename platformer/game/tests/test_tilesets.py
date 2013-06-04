import unittest
from game.settings.general_settings import TILE_SIZE
from game.tiles.tileset import TilesetConfig, TilesetImage, Tileset
from pyglet.image import TextureGrid, ImageGrid
from util.tileset import get_valid_config_data
from util.image import dummy_image

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










class TestTilesetImage(unittest.TestCase):
	"""Tests management of a tileset image."""

	def setUp(self):
		self.expected_tile_width = None
		self.expected_tile_height = None
		self.expected_rows = None
		self.expected_cols = None

		self.test_image = None
		self.tileset_image = None



	def test_unbounded_tileset_image(self):
		"""Tests creating a TilesetImage without specifying the rows and columns in the image."""
		# Create an 8x6 tileset image placeholder
		self.expected_tile_width = 8
		self.expected_tile_height = 6
		self.expected_rows = self.expected_tile_height
		self.expected_cols = self.expected_tile_width

		self.test_image = dummy_image(self.expected_width(), self.expected_height())
		self.test_image_grid = TextureGrid(ImageGrid(self.test_image, self.expected_rows, self.expected_cols))

		# Test creating a TilesetImage without specifying dimensions
		self.tileset_image = TilesetImage(self.test_image)

		self.assert_tileset_image('Rows and columns not specified.')

	def test_bounded_tileset_image(self):
		"""Tests creating a TilesetImage with specific rows and columns in the image."""
		# Create an 8x6 tileset image placeholder
		self.expected_tile_width = 8
		self.expected_tile_height = 6
		self.expected_rows = 5
		self.expected_cols = 4

		self.test_image = dummy_image(self.expected_width(), self.expected_height())
		self.test_image_grid = TextureGrid(ImageGrid(self.test_image, self.expected_rows, self.expected_cols))

		# Test creating a TilesetImage with specific dimensions
		self.tileset_image = TilesetImage(self.test_image, rows=self.expected_rows, cols=self.expected_cols)

		self.assert_tileset_image('Rows and columns not specified.')



	# Helper methods

	def assert_tileset_image(self, condition=''):
		"""Asserts that the tileset image coordinates are correct."""
		if condition:
			condition = ' Condition: '+condition

		# Check dimensions
		self.assertEqual(self.tileset_image.rows, self.expected_rows, "Tileset image has incorrect number of rows." + condition)
		self.assertEqual(self.tileset_image.cols, self.expected_cols, "Tileset image has incorrect number of columns." + condition)

		# Check retrieval of tile images

		# Test getting tile image at top left corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.top_left_tile_value()).tex_coords,
			self.test_image_grid[self.expected_rows-1, 0].tex_coords,
			"Tileset image has incorrect tile image for top left tile value." + condition
		)

		# Test getting tile image at bottom right corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.bottom_right_tile_value()).tex_coords,
			self.test_image_grid[0, self.expected_cols-1].tex_coords,
			"Tileset image has incorrect tile image for bottom right tile value." + condition
		)

		# Test getting tile image at top right corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.top_right_tile_value()).tex_coords,
			self.test_image_grid[self.expected_rows-1, self.expected_cols-1].tex_coords,
			"Tileset image has incorrect tile image for top right tile value." + condition
		)

		# Test getting tile image at bottom left corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.bottom_left_tile_value()).tex_coords,
			self.test_image_grid[0, 0].tex_coords,
			"Tileset image has incorrect tile image for bottom left tile value." + condition
		)

		# Check caching of tile image data

		first_call = self.tileset_image.get_tile_image_data(self.top_left_tile_value())
		second_call = self.tileset_image.get_tile_image_data(self.top_left_tile_value())

		self.assertIs(first_call, second_call, "Tileset image failed to cache image data for first tile value." + condition)

		# Check for a different tile value
		first_call = self.tileset_image.get_tile_image_data(self.bottom_right_tile_value())
		second_call = self.tileset_image.get_tile_image_data(self.bottom_right_tile_value())

		self.assertIs(first_call, second_call, "Tileset image failed to cache image data for second tile value." + condition)



	def expected_width(self):
		"""Returns the pixel width of the image for the current test dimensions."""
		return self.expected_tile_width * TILE_SIZE

	def expected_height(self):
		"""Returns the pixel height of the image for the current test dimensions."""
		return self.expected_tile_height * TILE_SIZE

	def top_right_tile_value(self):
		"""Returns the tile value of the top right tile image for the current test dimensions."""
		return self.expected_cols

	def top_left_tile_value(self):
		"""Returns the tile value of the top left tile image for the current test dimensions."""
		return 1

	def bottom_right_tile_value(self):
		"""Returns the tile value of the bottom right tile image for the current test dimensions."""
		return self.expected_rows * self.expected_cols

	def bottom_left_tile_value(self):
		"""Returns the tile value of the bottom left tile image for the current test dimensions."""
		return self.expected_cols * (self.expected_rows - 1) + 1










class TestTileset(unittest.TestCase):
	"""Tests the management of tileset images and configs."""

	def setUp(self):
		self.tileset = None



	def test_tileset_cache(self):
		"""Tests the caching of image and config data for a tileset."""
		test_image1 = dummy_image(6 * TILE_SIZE, 8 * TILE_SIZE)
		tileset_image1 = TilesetImage(test_image1)
		tileset_config1 = TilesetConfig(get_valid_config_data()['JSON'])

		test_image2 = dummy_image(10 * TILE_SIZE, 2 * TILE_SIZE)
		tileset_image2 = TilesetImage(test_image2)
		tileset_config2 = TilesetConfig('')

		# Create two different versions of the same tileset
		tileset1 = Tileset('test', tileset_image1, tileset_config1)
		tileset2 = Tileset('test', tileset_image2, tileset_config2)

		# Ensure that the cache works and was updated
		self.assertEqual('test', tileset1.name, "Tileset name was not set.")
		self.assertIs(tileset2.config, tileset_config2, "Tileset config cache was not updated.")
		self.assertIs(tileset2.image, tileset_image2, "Tileset image cache was not updated.")

	def test_tileset_tile_creation(self):
		"""Tests the creation of tiles via a tileset."""
		test_image = dummy_image(6 * TILE_SIZE, 8 * TILE_SIZE)
		tileset_image = TilesetImage(test_image)
		tileset_config = TilesetConfig(get_valid_config_data()['JSON'])

		self.tileset = Tileset('test', tileset_image, tileset_config)

		# Test tile creation

		# 1 is a custom tile which faces right
		test_tile = self.tileset.create_tile(1)

		self.assertEqual(test_tile.type, 'custom', "Tileset failed to create a custom tile.")
		self.assertEqual(test_tile.faces, 'right', "Tileset failed to create a custom tile facing the correct direction.")

		# 2 should be a basic tile
		test_tile = self.tileset.create_tile(2, x=32, y=64)

		self.assertEqual(test_tile.type, 'basic', "Tileset failed to create a basic tile.")
		self.assertEqual((test_tile.x, test_tile.y), (32, 64), "Tileset failed to pass additional arguments when creating tile.")

		# 3 should be a custom2 tile
		test_tile = self.tileset.create_tile(3)

		self.assertEqual(test_tile.type, 'custom2', "Tileset failed to create a custom2 tile.")

		# 5 should have its coordinates preset
		test_tile = self.tileset.create_tile(5)

		self.assertEqual((test_tile.x, test_tile.y), (32, 128), "Tileset failed to set coordinates of tile from tileset config.")

		# 7 should not be collidable
		test_tile = self.tileset.create_tile(7)

		self.assertEqual(test_tile.is_collidable, False, "Tileset failed to set is_collidable on tile from tileset config.")
