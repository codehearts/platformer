import unittest, math
from game.extended_sprite import ExtendedSprite
from game.settings.general_settings import TILE_SIZE
from pyglet.image import SolidColorImagePattern

class TestExtendedSprite(unittest.TestCase):
	"""Tests the ExtendedSprite class.

	These tests ensure that the additional positioning attributes that
	the class provides are always updated with the correct values.
	"""

	def setUp(self):
		"""Sets up variables for use with testing the ExtendedSprite class."""

		# Initial coordinates
		self.expected_x = None
		self.expected_y = None

		# Define the testing dimensions
		self.expected_width = None
		self.expected_height = None

		self.test_image = None
		self.test_sprite = None



	def test_square_sprite(self):
		"""Tests a square sprite."""
		# Run with square sprite
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE
		self.run_sprite_positioning_tests()
		self.run_sprite_dimension_tests()



	def test_tall_sprite(self):
		"""Tests a tall sprite."""
		# Run with tall sprite
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE * 3
		self.run_sprite_positioning_tests()
		self.run_sprite_dimension_tests()



	def test_wide_sprite(self):
		"""Tests a wide sprite."""
		# Run with tall sprite
		self.expected_width = TILE_SIZE * 3
		self.expected_height = TILE_SIZE
		self.run_sprite_positioning_tests()
		self.run_sprite_dimension_tests()



	def run_sprite_positioning_tests(self):
		"""Tests the positioning of an ExtendedSprite object."""
		self.test_image = SolidColorImagePattern().create_image(self.expected_width, self.expected_height)

		self.expected_x = TILE_SIZE * 3
		self.expected_y = TILE_SIZE

		self.test_sprite = ExtendedSprite(img=self.test_image, x=self.expected_x, y=self.expected_y)

		self.assert_coordinates('After tile initialization.')

		# Change the tile's lower left coordinates
		self.expected_x = self.expected_width
		self.expected_y = self.expected_height
		self.test_sprite.x = self.expected_x
		self.test_sprite.y = self.expected_y

		self.assert_coordinates('Moved via x and y attributes.')

		# Change the tile's upper right coordinates
		self.expected_x = self.expected_width * 2
		self.expected_y = self.expected_height * 2
		self.test_sprite.x2 = self.expected_x2()
		self.test_sprite.y2 = self.expected_y2()

		self.assert_coordinates('Moved via x2 and y2 attributes.')

		# Change the tile's lower left tile coordinates
		self.expected_x = self.expected_width * 4
		self.expected_y = self.expected_height * 5
		self.test_sprite.tile_x = self.expected_tile_x()
		self.test_sprite.tile_y = self.expected_tile_y()

		self.assert_coordinates('Moved via tile_x and tile_y attributes.')

		# Change the tile's upper right tile coordinates
		self.expected_x = self.expected_width * 8
		self.expected_y = self.expected_height * 2
		self.test_sprite.tile_x2 = self.expected_tile_x2()
		self.test_sprite.tile_y2 = self.expected_tile_y2()

		self.assert_coordinates('Moved via tile_x2 and tile_y2 attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 1.5
		self.expected_y = 15.725
		self.test_sprite.x = self.expected_x
		self.test_sprite.y = self.expected_y
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to x and y attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 3.1415
		self.expected_y = 0.9999
		self.test_sprite.x2 = self.expected_x2()
		self.test_sprite.y2 = self.expected_y2()
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to x2 and y2 attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 59.6
		self.expected_y = 2.171819
		self.test_sprite.tile_x = self.expected_tile_x()
		self.test_sprite.tile_y = self.expected_tile_y()
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to tile_x and tile_y attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 23.375
		self.expected_y = 348.408
		self.test_sprite.tile_x2 = self.expected_tile_x2()
		self.test_sprite.tile_y2 = self.expected_tile_y2()
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to tile_x2 and tile_y2 attributes.')



	def run_sprite_dimension_tests(self):
		"""Tests the dimensions of an ExtendedSprite object."""
		self.test_image = SolidColorImagePattern().create_image(self.expected_width, self.expected_height)

		self.test_sprite = ExtendedSprite(img=self.test_image, x=self.expected_x, y=self.expected_y)

		# Test pixel dimensions
		self.assertEqual(self.test_sprite.width, self.expected_width, "Sprite has incorrect width.")
		self.assertEqual(self.test_sprite.height, self.expected_height, "Sprite has incorrect height.")

		# Test tile dimensions
		self.assertEqual(self.test_sprite.tile_width, self.expected_tile_width(), "Sprite has incorrect tile width.")
		self.assertEqual(self.test_sprite.tile_height, self.expected_tile_height(), "Sprite has incorrect tile height.")



	# Helper methods



	def assert_coordinates(self, condition=''):
		"""Asserts that the tile coordinates are correct."""
		if condition:
			condition = ' Condition: '+condition

		# Test lower left coordinates
		self.assertEqual(self.test_sprite.x, self.expected_x, "Sprite has incorrect x coordinate." + condition)
		self.assertEqual(self.test_sprite.y, self.expected_y, "Sprite has incorrect y coordinate." + condition)

		# Test upper right coordinates
		self.assertEqual(self.test_sprite.x2, self.expected_x2(), "Sprite has incorrect x2 coordinate." + condition)
		self.assertEqual(self.test_sprite.y2, self.expected_y2(), "Sprite has incorrect y2 coordinate." + condition)

		# Test lower left tile coordinates
		self.assertEqual(self.test_sprite.tile_x, self.expected_tile_x(), "Sprite has incorrect tile x coordinate." + condition)
		self.assertEqual(self.test_sprite.tile_y, self.expected_tile_y(), "Sprite has incorrect tile y coordinate." + condition)

		# Test upper right tile coordinates
		self.assertEqual(self.test_sprite.tile_x2, self.expected_tile_x2(), "Sprite has incorrect tile x2 coordinate." + condition)
		self.assertEqual(self.test_sprite.tile_y2, self.expected_tile_y2(), "Sprite has incorrect tile y2 coordinate." + condition)

	def expected_x2(self):
		"""Returns x2 for the current test coordinate values."""
		return self.expected_x + self.expected_width

	def expected_y2(self):
		"""Returns y2 for the current test coordinate values."""
		return self.expected_y + self.expected_height

	def expected_tile_x(self):
		"""Returns tile_x for the current test coordinate values."""
		return self.expected_x / TILE_SIZE

	def expected_tile_y(self):
		"""Returns tile_y for the current test coordinate values."""
		return self.expected_y / TILE_SIZE

	def expected_tile_x2(self):
		"""Returns tile_x2 for the current test coordinate values."""
		return self.expected_x2() / TILE_SIZE

	def expected_tile_y2(self):
		"""Returns tile_y2 for the current test coordinate values."""
		return self.expected_y2() / TILE_SIZE

	def expected_tile_width(self):
		"""Returns tile_width for the current test coordinate values."""
		return math.ceil(self.expected_width / TILE_SIZE)

	def expected_tile_height(self):
		"""Returns tile_height for the current test coordinate values."""
		return math.ceil(self.expected_height / TILE_SIZE)
