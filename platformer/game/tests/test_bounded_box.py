import unittest
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE
from util import bounded_box

# TODO Test bounded box attributes with fixed data (use hardcoded numbers instead of methods which predict the expected value)
# TODO Ensure that these values are correct when in negative quadrants
class TestBoundedBox(unittest.TestCase):
	"""Tests the :class:`game.bounded_box.BoundedBox` class.

	These tests ensure that the positioning attributes that the class
	provides are always up to date with the correct values.

	The :mod:`game.tests.util.bounded_box` module provides utilities
	for easily writing extensive tests for BoundedBox and its subclasses.
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



	def create_box(self, x, y, width, height):
		"""Creates a BoundedBox object for testing."""
		return BoundedBox(x, y, width, height)



	def test_square_box(self):
		"""Tests a square BoundedBox."""
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE
		bounded_box.run_positioning_tests(self)
		bounded_box.run_dimension_tests(self)



	def test_tall_box(self):
		"""Tests a tall BoundedBox."""
		self.expected_width = TILE_SIZE
		# TODO Don't just use clean multiples of the tile size
		self.expected_height = TILE_SIZE * 3
		bounded_box.run_positioning_tests(self)
		bounded_box.run_dimension_tests(self)



	def test_wide_box(self):
		"""Tests a wide BoundedBox."""
		self.expected_width = TILE_SIZE * 3
		self.expected_height = TILE_SIZE
		bounded_box.run_positioning_tests(self)
		bounded_box.run_dimension_tests(self)



	def test_x2_tile(self):
		"""Tests the x2_tile property of a BoundedBox."""
		# TODO Same thing on y-axis
		self.test_box = self.create_box(0, 0, TILE_SIZE * 2, TILE_SIZE)
		self.assertEqual(self.test_box.x2_tile, 1,
			"x2_tile of 2-tile wide box at (0,0) is not on the second tile.")

		self.test_box = self.create_box(1, 0, TILE_SIZE * 2, TILE_SIZE)
		self.assertEqual(self.test_box.x2_tile, 2,
			"x2_tile of 2-tile wide box at (1,0) is not on the third tile.")

		self.test_box = self.create_box(0, 0, TILE_SIZE * 1.5, TILE_SIZE)
		self.assertEqual(self.test_box.x2_tile, 1,
			"x2_tile of 1.5-tile wide box at (0,0) is not on the second tile.")

		self.test_box = self.create_box(TILE_SIZE/2, 0, TILE_SIZE * 1.5, TILE_SIZE)
		self.assertEqual(self.test_box.x2_tile, 1,
			"x2_tile of 1.5-tile wide box at (TILE_SIZE/2,0) is not on the second tile.")

		self.test_box = self.create_box(TILE_SIZE/2 + 1, 0, TILE_SIZE * 1.5, TILE_SIZE)
		self.assertEqual(self.test_box.x2_tile, 2,
			"x2_tile of 1.5-tile wide box at (TILE_SIZE/2 + 1,0) is not on the third tile.")



	def test_bounding_within(self):
		"""Tests bounding a BoundedBox within another BoundedBox."""
		bounded_box.run_bounding_within_tests(self)



	def test_box_equality(self):
		"""Tests checking for the equality of BoundedBoxes."""
		bounded_box.run_box_equality_tests(self)
