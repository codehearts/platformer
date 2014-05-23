import unittest
from game.tiles.tileset import tileset_loaders
from pyglet.resource import ResourceNotFoundException
from ..util import resource

class TestTilesetLoaders(unittest.TestCase):
	"""Tests resource loaders for tilesets."""

	@classmethod
	def setUpClass(cls):
		resource.setUp()

	@classmethod
	def tearDownClass(cls):
		resource.tearDown()



	def test_load_tileset_file(self):
		"""Ensures that arbitrary tileset files can be opened."""
		# Test that no exceptions are raised when opening a tileset file
		tileset_loaders.load_tileset_file('config-test', 'arbitrary.txt')

		# Test that an exception is raised when opening a nonexistent file
		try:
			self.assertRaises(
				ResourceNotFoundException,
				tileset_loaders.load_tileset_file,
				'config-test',
				'does-not-exist.txt'
			)
		except AssertionError:
			raise AssertionError("ResourceNotFoundException not raised when attempting to load nonexistent tileset file.")

		# Test that an exception is raised when opening a file from
		# a nonexistent tileset
		try:
			self.assertRaises(
				ResourceNotFoundException,
				tileset_loaders.load_tileset_file,
				'does-not-exist',
				'config.json'
			)
		except AssertionError:
			raise AssertionError("ResourceNotFoundException not raised when attempting to load a file from a nonexistent tileset.")



	def test_config_loader(self):
		"""Ensures that the config loader can successfully read config files.
		Also ensures that nonexistent config files result in an empty string
		being returned without raising an exception.
		"""
		# Test getting the config file contents from a tileset with a config
		expected_contents = ('{\n'
			'\t"1": {\n'
			'\t\t"type": "basic"\n'
			'\t},\n'
			'\t"6": {\n'
			'\t\t"type": "custom",\n'
			'\t\t"faces": "down"\n'
			'\t}\n'
			'}\n'
		)
		actual_contents = tileset_loaders.get_tileset_config('config-test')

		self.assertEqual(expected_contents, actual_contents,
			"Tileset config loader returned incorrect file contents.")

		# Ensure that loading a nonexistent config returns an empty string
		# and does not raise an exception
		self.assertEqual('', tileset_loaders.get_tileset_config('no-config'),
			"Tileset config loader did not return an empty string for a nonexistent config.")




	def test_load_tileset_image(self):
		"""Ensures that arbitrary tileset image files can be opened."""
		# Test that no exceptions are raised when opening a tileset image
		tileset_loaders.load_tileset_image('image-test', 'tiles.png')

		# Test that an exception is raised when opening a nonexistent file
		try:
			self.assertRaises(
				ResourceNotFoundException,
				tileset_loaders.load_tileset_image,
				'image-test',
				'does-not-exist.png'
			)
		except AssertionError:
			raise AssertionError("ResourceNotFoundException not raised when attempting to load nonexistent tileset image file.")

		# Test that an exception is raised when opening a file from
		# a nonexistent tileset
		try:
			self.assertRaises(
				ResourceNotFoundException,
				tileset_loaders.load_tileset_image,
				'does-not-exist',
				'tiles.png'
			)
		except AssertionError:
			raise AssertionError("ResourceNotFoundException not raised when attempting to load tileset image file from nonexistent tileset.")



	def test_image_loader(self):
		"""Ensures that a tileset image will be loaded if it is in any
		of the acceptable formats."""
		# TODO FIXME (Broken on Linux) Test loading a from a tileset which only has a gif
		#tileset_loaders.get_tileset_image('gif-only')
		# Test loading a from a tileset which only has a png
		tileset_loaders.get_tileset_image('png-only')
		# TODO FIXME (Broken on Linux) Test loading a from a tileset which only has a jpg
		#tileset_loaders.get_tileset_image('jpg-only')
		# TODO FIXME (Broken on Linux) Test loading a from a tileset which only has a jpeg
		#tileset_loaders.get_tileset_image('jpeg-only')

		# Test that an exception is raised when attempting to open a
		# tileset image when on does not exist
		try:
			self.assertRaises(
				ResourceNotFoundException,
				tileset_loaders.get_tileset_image,
				'no-image'
			)
		except AssertionError:
			raise AssertionError("ResourceNotFoundException not raised when attempting to load a tileset image from a tileset which has no image.")
