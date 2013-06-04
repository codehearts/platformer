import unittest

class TestTilesetLoaders(unittest.TestCase):
	"""Tests resource loaders for tilesets."""

	def setUp(self):
		# TODO Set pyglet resource path to be within test dir
		# TODO Set tilesets directory, just to be safe
		pass

	def test_config_loader_path(self):
		"""Ensures that the correct tileset config path is always returned."""
		# TODO Test getting the expected config path
		pass

	def test_config_loader(self):
		"""Ensures that the config loader can successfully read config files.
		Also ensures that nonexistent config files result in an empty string
		being returned without raising an exception.
		"""
		# TODO Test loading a config with known contents
		# TODO Test loading a nonexistent config
		# TODO Assert loading nonexistent config doesn't raise exception
		pass

	def test_image_loader_path(self):
		"""Ensures that the correct tileset image path is always returned."""
		# TODO Test getting the expected image path
		pass

	def test_image_loader(self):
		"""Ensures that a tileset image will be loaded if it is in any
		of the acceptable formats."""
		# TODO Test loading a gif
		# TODO Test loading a png
		# TODO Test loading a jpeg
		# TODO Test loading a jpg
		# TODO Assert loading nonexistent image raises exception
		pass
