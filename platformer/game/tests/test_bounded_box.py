import unittest
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE
from util import bounded_box

class TestBoundedBox(unittest.TestCase):
	"""Tests the BoundedBox class.

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
		"""Tests a square box."""
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE
		bounded_box.run_positioning_tests(self)
		bounded_box.run_dimension_tests(self)



	def test_tall_box(self):
		"""Tests a tall box."""
		self.expected_width = TILE_SIZE
		self.expected_height = TILE_SIZE * 3
		bounded_box.run_positioning_tests(self)
		bounded_box.run_dimension_tests(self)



	def test_wide_box(self):
		"""Tests a wide box."""
		self.expected_width = TILE_SIZE * 3
		self.expected_height = TILE_SIZE
		bounded_box.run_positioning_tests(self)
		bounded_box.run_dimension_tests(self)



	def test_bounding_within(self):
		"""Tests bounding a BoundedBox within another BoundedBox."""
		bounded_box.run_bounding_within_tests(self)



	def test_box_equality(self):
		"""Tests checking for the equality of bounded boxes."""
		bounded_box.run_box_equality_tests(self)
