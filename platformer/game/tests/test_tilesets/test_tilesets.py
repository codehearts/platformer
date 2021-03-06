import unittest
from game.settings.general_settings import TILE_SIZE
from game.tiles.tileset import TilesetConfig, TilesetImage, Tileset, tileset_loaders
from ..util import resource
from ..util.image import dummy_image
from ..util.tileset import get_valid_config_data, get_testing_tileset_config, get_testing_tileset_image

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



	def test_tileset_loading(self):
		"""Tests loading a tileset by name."""
		# Set up testing resources
		resource.setUp()

		# Attempt to load the test tileset
		self.tileset = Tileset.load('load-test')

		config_file = tileset_loaders.get_tileset_config('load-test')
		expected_config = TilesetConfig(config_file)

		# Test that the correct config data was loaded
		# We're not testing the image against an expected image  because
		# it's a pain to write image comparison tests and if the proper
		# config was loaded, the proper image should have been as well.
		self.assertEqual(expected_config, self.tileset.config,
			"Tileset.load() loaded wrong config file.")

		# Ensure that the loaded data was cached
		tileset2 = Tileset.load('load-test')
		self.assertIs(tileset2.image, self.tileset.image,
			"Tileset.load() did not cache image file contents.")
		self.assertIs(tileset2.config, self.tileset.config,
			"Tileset.load() did not cache config file contents.")

		# Tear down testing resources
		resource.tearDown()



	def test_tileset_cache_flush(self):
		"""Tests clearing the tileset cache."""
		# Set up testing resources
		resource.setUp()

		# Ensure the cache is empty
		Tileset.flush_cache()

		# Create our own tileset data
		# This data will be cached for the specified tileset, and so
		# subsequent calls to load that tileset will return the cached data
		test_image = get_testing_tileset_image(6, 8)
		test_config = get_testing_tileset_config()
		self.tileset = Tileset('test', test_image, test_config)

		# Load the test tileset
		# Because we already created a test tileset, that data was
		# cached and so instead of reading the tileset files,
		# it should use that cached data
		loaded_tileset = Tileset.load('test')

		# Ensure that the data was cached
		self.assertIs(loaded_tileset.image, test_image,
			"Tileset.load() failed to use cached image data.")
		self.assertIs(loaded_tileset.config, test_config,
			"Tileset.load() failed to use cached config data.")

		# Clear the cache for this tileset
		self.tileset.empty_cache()

		# Ensure that our data is still there
		self.assertIs(loaded_tileset.image, test_image,
			"Tileset.load() failed to use cached image data.")
		self.assertIs(loaded_tileset.config, test_config,
			"Tileset.load() failed to use cached config data.")

		# Reload the tileset. Because we cleared the cached data,
		# this should read the tileset files from disk
		loaded_tileset = Tileset.load('test')

		# Ensure that new data was loaded
		self.assertIsNot(loaded_tileset.image, test_image,
			"Tileset.load() failed to load new image data after cache flush.")
		self.assertIsNot(loaded_tileset.config, test_config,
			"Tileset.load() failed to load new config data after cache flush.")

		# Tear down testing resources
		resource.tearDown()
