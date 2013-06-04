import unittest
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE, TILE_SIZE_FLOAT
from math import ceil

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



	def test_bounding_within(self):
		"""Tests bounding a BoundedBox within another BoundedBox."""
		# Larger than test box by 10 pixels on every side
		larger_box = BoundedBox(-10, -10, 52, 52)

		# Test bounding within a larger box
		self.reset_test_box()
		self.expected_x = self.test_box.x
		self.expected_y = self.test_box.y
		self.expected_width = self.test_box.width
		self.expected_height = self.test_box.height

		self.test_box.bound_within(larger_box)
		self.assert_coordinates('Bounded within a larger box.')
		self.assert_dimensions('Bounded within a larger box.')

		# Test bounding with a box that is entirely within the test box
		smaller_box = BoundedBox(10, 10, 12, 12)

		self.reset_test_box()
		self.expected_x = 10
		self.expected_y = 10
		self.expected_width = self.test_box.width - 20
		self.expected_height = self.test_box.height - 20

		self.test_box.bound_within(smaller_box)
		self.assert_coordinates('Bounded within a smaller box.')
		self.assert_dimensions('Bounded within a smaller box.')

		# Overlaps upper right corner of test box only
		upper_right_overlap_box = BoundedBox(10, 10, 32, 32)

		self.reset_test_box()
		self.expected_x = 10
		self.expected_y = 10
		self.expected_width = self.test_box.width - 10
		self.expected_height = self.test_box.height - 10

		self.test_box.bound_within(upper_right_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps upper right corner.')
		self.assert_dimensions('Bounded within a box which overlaps upper right corner.')

		# Overlaps upper left corner of test box only
		upper_left_overlap_box = BoundedBox(-10, 10, 32, 32)

		self.reset_test_box()
		self.expected_x = 0
		self.expected_y = 10
		self.expected_width = self.test_box.width - 10
		self.expected_height = self.test_box.height - 10

		self.test_box.bound_within(upper_left_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps upper left corner.')
		self.assert_dimensions('Bounded within a box which overlaps upper left corner.')

		# Overlaps lower right corner of test box only
		lower_right_overlap_box = BoundedBox(10, -10, 32, 32)

		self.reset_test_box()
		self.expected_x = 10
		self.expected_y = 0
		self.expected_width = self.test_box.width - 10
		self.expected_height = self.test_box.height - 10

		self.test_box.bound_within(lower_right_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps lower right corner.')
		self.assert_dimensions('Bounded within a box which overlaps lower right corner.')

		# Overlaps lower left corner of test box only
		lower_left_overlap_box = BoundedBox(-10, -10, 32, 32)

		self.reset_test_box()
		self.expected_x = 0
		self.expected_y = 0
		self.expected_width = self.test_box.width - 10
		self.expected_height = self.test_box.height - 10

		self.test_box.bound_within(lower_left_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps lower left corner.')
		self.assert_dimensions('Bounded within a box which overlaps lower left corner.')

		# Overlaps top of test box only
		top_overlap_box = BoundedBox(0, 16, 32, 32)

		self.reset_test_box()
		self.expected_x = 0
		self.expected_y = 16
		self.expected_width = self.test_box.width
		self.expected_height = self.test_box.height - 16

		self.test_box.bound_within(top_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps top side.')
		self.assert_dimensions('Bounded within a box which overlaps top side.')

		# Overlaps bottom of test box only
		bottom_overlap_box = BoundedBox(0, 0, 32, 16)

		self.reset_test_box()
		self.expected_x = 0
		self.expected_y = 0
		self.expected_width = self.test_box.width
		self.expected_height = self.test_box.height - 16

		self.test_box.bound_within(bottom_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps bottom side.')
		self.assert_dimensions('Bounded within a box which overlaps bottom side.')

		# Overlaps left of test box only
		left_overlap_box = BoundedBox(0, 0, 16, 32)

		self.reset_test_box()
		self.expected_x = 0
		self.expected_y = 0
		self.expected_width = self.test_box.width - 16
		self.expected_height = self.test_box.height

		self.test_box.bound_within(left_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps left side.')
		self.assert_dimensions('Bounded within a box which overlaps left side.')

		# Overlaps right of test box only
		right_overlap_box = BoundedBox(16, 0, 16, 32)

		self.reset_test_box()
		self.expected_x = 16
		self.expected_y = 0
		self.expected_width = self.test_box.width - 16
		self.expected_height = self.test_box.height

		self.test_box.bound_within(right_overlap_box)
		self.assert_coordinates('Bounded within a box which overlaps right side.')
		self.assert_dimensions('Bounded within a box which overlaps right side.')

	def test_box_equality(self):
		"""Tests checking for the equality of bounded boxes."""
		box1 = BoundedBox(0, 0, 32, 32)
		box2 = BoundedBox(0, 0, 32, 32)
		box3 = BoundedBox(32, 32, 128, 64)

		self.assertEqual(box1, box2, "Similar boxes claimed to be unequal.")
		self.assertNotEqual(box1, box3, "Different boxes claimed to be equal.")
		self.assertNotEqual(box2, box3, "Different boxes claimed to be equal.")

		# Test after a box's position has changed to be different from all other boxes
		box2.x = 16
		self.assertNotEqual(box1, box2, "Different boxes claimed to be equal after similar box was changed to be different.")
		self.assertNotEqual(box2, box3, "Different boxes claimed to be equal after different box was changed to remain different.")

		# Test after a box has been changed to be similar to another box
		box2.x = 32
		box2.y = 32
		box2.width = 128
		box2.height = 64
		self.assertNotEqual(box1, box2, "Different boxes claimed to be equal after different box was changed to remain different.")
		self.assertEqual(box2, box3, "Similar boxes claimed to be unequal after different box was changed to be similar.")




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

		# Change the tile's lower left tile index
		self.expected_x = int(3.25 * TILE_SIZE)
		self.expected_y = int(4.1 * TILE_SIZE)
		self.test_box.x_tile = 3.25
		self.test_box.y_tile = 4.1

		self.assert_coordinates('Moved via x_tile and y_tile attributes.')

		# Change the tile's upper right tile index
		self.expected_x = 5 * TILE_SIZE - self.expected_width
		self.expected_y = ceil(2.5 * TILE_SIZE) - self.expected_height
		self.test_box.x2_tile = 5
		self.test_box.y2_tile = 2.5

		self.assert_coordinates('Moved via x2_tile and y2_tile attributes.')

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

		# Resize the box via tile_width_span and tile_height_span
		self.expected_width = int(4 * TILE_SIZE_FLOAT)
		self.expected_height = int(ceil(1.25) * TILE_SIZE_FLOAT)
		self.test_box.tile_width_span = 4
		self.test_box.tile_height_span = 1.25

		# Ensure that the dimensions and any coordinates depending on the dimensions were updated
		self.assert_dimensions('Box was resized via tile_width_span and tile_height_span attributes.')
		self.assert_coordinates('Box was resized via tile_width_span and tile_height_span attributes.')



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

		# Test tile of lower left coordinates
		self.assertEqual(self.test_box.x_tile, self.expected_x_tile(), "Box has incorrect x_tile index." + condition)
		self.assertEqual(self.test_box.y_tile, self.expected_y_tile(), "Box has incorrect y_tile index." + condition)

		# Test tile of upper right coordinates
		self.assertEqual(self.test_box.x2_tile, self.expected_x2_tile(), "Box has incorrect x2_tile index." + condition)
		self.assertEqual(self.test_box.y2_tile, self.expected_y2_tile(), "Box has incorrect y2_tile index." + condition)

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

		# Test tile span dimensions
		self.assertEqual(self.test_box.tile_width_span, self.expected_tile_width_span(), "Box has incorrect tile width span." + condition)
		self.assertEqual(self.test_box.tile_height_span, self.expected_tile_height_span(), "Box has incorrect tile height span." + condition)



	def reset_test_box(self):
		"""Resets the test box to a 32x32 pixel box at (0,0)"""
		self.test_box = BoundedBox(0, 0, 32, 32)

	def expected_x2(self):
		"""Returns x2 for the current test coordinate values."""
		return self.expected_x + self.expected_width

	def expected_y2(self):
		"""Returns y2 for the current test coordinate values."""
		return self.expected_y + self.expected_height

	def expected_x_tile(self):
		"""Returns x_tile for the current test coordinate values."""
		return int(self.expected_tile_x())

	def expected_y_tile(self):
		"""Returns y_tile for the current test coordinate values."""
		return int(self.expected_tile_y())

	def expected_x2_tile(self):
		"""Returns x2_tile for the current test coordinate values."""
		return int(ceil(self.expected_tile_x2()))

	def expected_y2_tile(self):
		"""Returns y2_tile for the current test coordinate values."""
		return int(ceil(self.expected_tile_y2()))

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

	def expected_tile_width_span(self):
		"""Returns tile_width_span for the current test coordinate values."""
		return ceil(self.expected_tile_width())

	def expected_tile_height_span(self):
		"""Returns tile_height_span for the current test coordinate values."""
		return ceil(self.expected_tile_height())
