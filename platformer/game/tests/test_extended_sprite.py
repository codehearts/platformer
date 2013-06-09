import unittest
from game.extended_sprite import ExtendedSprite
from game.settings.general_settings import TILE_SIZE
from util import bounded_box
from util.image import dummy_image

class TestExtendedSprite(unittest.TestCase):
	"""Tests the :class:`game.extended_sprite.ExtendedSprite` class.

	These tests ensure that the positioning attributes that the class
	provides are always up to date with the correct values.

	The :mod:`game.tests.util.bounded_box` module provides utilities
	for easily writing extensive tests for BoundedBox and its subclasses.
	"""

	def setUp(self):
		"""Sets up variables for use with testing the ExtendedSprite class."""

		# Initial coordinates
		self.expected_x = None
		self.expected_y = None

		# Define the testing dimensions
		self.expected_width = None
		self.expected_height = None

		self.test_box = None



	def create_box(self, x, y, width, height):
		"""Creates an ExtendedSprite object for testing."""
		return ExtendedSprite(dummy_image(width, height), x=x, y=y)



	def test_square_sprite(self):
		"""Tests a square ExtendedSprite."""
		self.expected_width = 1 * TILE_SIZE
		self.expected_height = 1 * TILE_SIZE
		bounded_box.run_positioning_tests(self)

	def test_tall_sprite(self):
		"""Tests a tall ExtendedSprite."""
		self.expected_width = 1 * TILE_SIZE
		self.expected_height = 3 * TILE_SIZE
		bounded_box.run_positioning_tests(self)

	def test_wide_sprite(self):
		"""Tests a wide ExtendedSprite."""
		self.expected_width = 3 * TILE_SIZE
		self.expected_height = 1 * TILE_SIZE
		bounded_box.run_positioning_tests(self)
