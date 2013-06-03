import unittest
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE, TILE_SIZE_FLOAT

class TestBoundedBox(unittest.TestCase):
	"""Tests the BoundedBox class.

	These tests ensure that the positioning attributes that the class
	provides are always update to date with the correct values.
	"""

	def setUp(self):
		"""Sets up variables for use with testing the BoundedBox class."""

		# Initial coordinates
		self.expected_x = None
		self.expected_y = None

		# Define the testing dimensions
		self.expected_width = None
		self.expected_height = None

		self.test_box = None



	def test_square_box(self):
		"""Tests a square box."""
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE
		self.run_positioning_tests()
		self.run_dimension_tests()



	def test_tall_box(self):
		"""Tests a tall box."""
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE * 3
		self.run_positioning_tests()
		self.run_dimension_tests()



	def test_wide_box(self):
		"""Tests a wide box."""
		self.expected_width = TILE_SIZE * 3
		self.expected_height = TILE_SIZE
		self.run_positioning_tests()
		self.run_dimension_tests()



	def run_positioning_tests(self):
		"""Tests the positioning of a BoundedBox object."""
		self.expected_x = TILE_SIZE * 3
		self.expected_y = TILE_SIZE

		self.test_box = BoundedBox(self.expected_x, self.expected_y, self.expected_width, self.expected_height)

		self.assert_coordinates('After tile initialization.')

		# Change the tile's lower left coordinates
		self.expected_x = self.expected_width
		self.expected_y = self.expected_height
		self.test_box.x = self.expected_x
		self.test_box.y = self.expected_y

		self.assert_coordinates('Moved via x and y attributes.')

		# Change the tile's upper right coordinates
		self.expected_x = self.expected_width * 2
		self.expected_y = self.expected_height * 2
		self.test_box.x2 = self.expected_x2()
		self.test_box.y2 = self.expected_y2()

		self.assert_coordinates('Moved via x2 and y2 attributes.')

		# Change the tile's lower left tile coordinates
		self.expected_x = self.expected_width * 4
		self.expected_y = self.expected_height * 5
		self.test_box.tile_x = self.expected_tile_x()
		self.test_box.tile_y = self.expected_tile_y()

		self.assert_coordinates('Moved via tile_x and tile_y attributes.')

		# Change the tile's upper right tile coordinates
		self.expected_x = self.expected_width * 8
		self.expected_y = self.expected_height * 2
		self.test_box.tile_x2 = self.expected_tile_x2()
		self.test_box.tile_y2 = self.expected_tile_y2()

		self.assert_coordinates('Moved via tile_x2 and tile_y2 attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 1.5
		self.expected_y = 15.725
		self.test_box.x = self.expected_x
		self.test_box.y = self.expected_y
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to x and y attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 3.1415
		self.expected_y = 0.9999
		self.test_box.x2 = self.expected_x2()
		self.test_box.y2 = self.expected_y2()
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to x2 and y2 attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 59.6
		self.expected_y = 2.171819
		self.test_box.tile_x = self.expected_tile_x()
		self.test_box.tile_y = self.expected_tile_y()
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to tile_x and tile_y attributes.')

		# Change the tile's coordinates with floats
		self.expected_x = 23.375
		self.expected_y = 348.408
		self.test_box.tile_x2 = self.expected_tile_x2()
		self.test_box.tile_y2 = self.expected_tile_y2()
		self.expected_x = int(self.expected_x)
		self.expected_y = int(self.expected_y)

		self.assert_coordinates('Moved via passing float to tile_x2 and tile_y2 attributes.')



	def run_dimension_tests(self):
		"""Tests the dimensions of a BoundedBox object."""
		self.test_box = BoundedBox(self.expected_x, self.expected_y, self.expected_width, self.expected_height)

		self.assert_dimensions('Box was initialized.')

		# Expand the box via width and height
		self.expected_width += self.expected_width / 2
		self.expected_height += self.expected_height / 2
		self.test_box.width = self.expected_width
		self.test_box.height = self.expected_height

		# Ensure that the dimensions and any coordinates depending on the dimensions were updated
		self.assert_dimensions('Box was expanded via width and height attributes.')
		self.assert_coordinates('Box was expanded via width and height attributes.')

		# Shrink the box via tile_width and tile_height
		self.expected_width -= self.expected_width / 2
		self.expected_height -= self.expected_height / 2
		self.test_box.tile_width = self.expected_width / TILE_SIZE_FLOAT
		self.test_box.tile_height = self.expected_height / TILE_SIZE_FLOAT

		# Ensure that the dimensions and any coordinates depending on the dimensions were updated
		self.assert_dimensions('Box was shrunk via tile_width and tile_height attributes.')
		self.assert_coordinates('Box was shrunk via tile_width and tile_height attributes.')



	# Helper methods



	def assert_coordinates(self, condition=''):
		"""Asserts that the box's coordinates are correct."""
		if condition:
			condition = ' Condition: '+condition

		# Test lower left coordinates
		self.assertEqual(self.test_box.x, self.expected_x, "Box has incorrect x coordinate." + condition)
		self.assertEqual(self.test_box.y, self.expected_y, "Box has incorrect y coordinate." + condition)

		# Test upper right coordinates
		self.assertEqual(self.test_box.x2, self.expected_x2(), "Box has incorrect x2 coordinate." + condition)
		self.assertEqual(self.test_box.y2, self.expected_y2(), "Box has incorrect y2 coordinate." + condition)

		# Test lower left tile coordinates
		self.assertEqual(self.test_box.tile_x, self.expected_tile_x(), "Box has incorrect tile x coordinate." + condition)
		self.assertEqual(self.test_box.tile_y, self.expected_tile_y(), "Box has incorrect tile y coordinate." + condition)

		# Test upper right tile coordinates
		self.assertEqual(self.test_box.tile_x2, self.expected_tile_x2(), "Box has incorrect tile x2 coordinate." + condition)
		self.assertEqual(self.test_box.tile_y2, self.expected_tile_y2(), "Box has incorrect tile y2 coordinate." + condition)

	def assert_dimensions(self, condition=''):
		"""Asserts that the box's dimensions are correct."""
		if condition:
			condition = ' Condition: '+condition

		# Test pixel dimensions
		self.assertEqual(self.test_box.width, self.expected_width, "Box has incorrect width." + condition)
		self.assertEqual(self.test_box.height, self.expected_height, "Box has incorrect height." + condition)

		# Test tile dimensions
		self.assertEqual(self.test_box.tile_width, self.expected_tile_width(), "Box has incorrect tile width." + condition)
		self.assertEqual(self.test_box.tile_height, self.expected_tile_height(), "Box has incorrect tile height." + condition)

	def expected_x2(self):
		"""Returns x2 for the current test coordinate values."""
		return self.expected_x + self.expected_width

	def expected_y2(self):
		"""Returns y2 for the current test coordinate values."""
		return self.expected_y + self.expected_height

	def expected_tile_x(self):
		"""Returns tile_x for the current test coordinate values."""
		return self.expected_x / TILE_SIZE_FLOAT

	def expected_tile_y(self):
		"""Returns tile_y for the current test coordinate values."""
		return self.expected_y / TILE_SIZE_FLOAT

	def expected_tile_x2(self):
		"""Returns tile_x2 for the current test coordinate values."""
		return self.expected_x2() / TILE_SIZE_FLOAT

	def expected_tile_y2(self):
		"""Returns tile_y2 for the current test coordinate values."""
		return self.expected_y2() / TILE_SIZE_FLOAT

	def expected_tile_width(self):
		"""Returns tile_width for the current test coordinate values."""
		return self.expected_width / TILE_SIZE_FLOAT

	def expected_tile_height(self):
		"""Returns tile_height for the current test coordinate values."""
		return self.expected_height / TILE_SIZE_FLOAT
