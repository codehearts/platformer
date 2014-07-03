from game.settings.general_settings import TILE_SIZE, FRAME_LENGTH, FPS
from game.physical_objects.physical_object import PhysicalObject
from game.tiles import TileMap, Tileset
from game.tiles.tileset import TilesetImage, TilesetConfig
from util.tileset import get_testing_tileset
from util.image import dummy_image
import unittest

class TestSlopeCollisions(unittest.TestCase):
	"""Tests that object collisions with slopes are resolved as expected."""

	def setUp(self):
		# The map is upside down
		# TODO Write a method to take a tile map list and "load" it
		slope_map = [
			[ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 0
			[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00], # 1
			[00,00,00,00, 4, 5,00,00,00, 6, 7,00,00,00,00, 2,00, 3,00,00,00,00], # 2
			[00,00,00,00,00,00, 2,00, 3,00,00,00,00,00,00,00,00,00,00,00,00,00], # 3
			[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00], # 4
			[ 6, 7, 3, 6, 7,00,00,00,00,00, 4, 5, 2, 4, 5,00,00, 2, 2, 3, 3,00], # 5
			[00,00,00,00,00, 2,00, 1,00,10,00,00,00,00,00,00,00,00,00,00,00,00], # 6
			[00,00,00,00,00,00, 2,00, 3,00,00,00,00, 1, 4, 5, 6, 7, 1,00,00,00], # 7
			# 0	 1	2  3  4	 5	6  7  8	 9 10 11 12 13 14 15 16 17 18 19 20 21
		]

		tileset_image = TilesetImage(dummy_image(6 * TILE_SIZE, 8 * TILE_SIZE))
		tileset_config = TilesetConfig('{\
			"2": {\
				"type": "slope",\
				"left_height": 0,\
				"right_height": 32\
			},\
			"3": {\
				"type": "slope",\
				"left_height": 32,\
				"right_height": 0\
			},\
			"4": {\
				"type": "slope",\
				"left_height": 0,\
				"right_height": 16\
			},\
			"5": {\
				"type": "slope",\
				"left_height": 17,\
				"right_height": 32\
			},\
			"6": {\
				"type": "slope",\
				"left_height": 32,\
				"right_height": 17\
			},\
			"7": {\
				"type": "slope",\
				"left_height": 16,\
				"right_height": 0\
			}\
		}')

		slope_level = TileMap(slope_map, Tileset('slope-test', tileset_image, tileset_config))

		self.obj = PhysicalObject(slope_level.tiles, dummy_image(TILE_SIZE, TILE_SIZE), TILE_SIZE*6, TILE_SIZE*5, mass=100)
		self.half_width = float(self.obj.half_width)
		self.half_tile_width = self.half_width / TILE_SIZE

	def _simulate_time(self, seconds, update_object):
		"""Simulates time by calling the given update function every frame for the given amount of time."""
		map(lambda x: update_object.update(FRAME_LENGTH), xrange(int(FPS * seconds)))

	def _assert_slope_resolution(self, expected_tiles, locations, movement, slope_type):
		"""Asserts that the object has resolved to the expected coordinates on the slope tile.

		Args:
			expected_tiles (tuple of float): The expected tile coordinates of the object after resolution.
			locations (tuple of str): A description of the expected x and y locations on the slope.
			movement (str): A description of the object's movement onto the slope.
			slope_type (str): A description of the tile the object has moved onto.
		"""
		self._simulate_time(1, self.obj)

		self.assertEqual(expected_tiles[0]*TILE_SIZE, self.obj.x,
			"Object's x position is not {0} tile after moving {1} onto {2} slope. Expected {3} but got {4}.".format(
			locations[0], movement, slope_type, expected_tiles[0]*TILE_SIZE, self.obj.x))
		self.assertEqual(expected_tiles[1]*TILE_SIZE, self.obj.y,
			"Object's y position is not {0} tile after moving {1} onto {2} slope. Expected {3} but got {4}.".format(
			locations[1], movement, slope_type, expected_tiles[1]*TILE_SIZE, self.obj.y))

	def _assert_slope_jump_resolution(self, expected_y_tile, location, slope_type):
		"""Asserts that the object has resolved above the expected coordinates when jumping from a slope tile.

		Args:
			expected_tile_y (float): The expected tile coordinate of the object after resolution.
			location (str): A description of the object's location on the slope before jumping.
			slope_type (str): A description of the type of slope being jumped from.
		"""
		self._simulate_time(0.5, self.obj) # Give the object time to settle
		self.obj.jump()
		self._simulate_time(0.25, self.obj) # Give the object time to jump up

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(self.obj.y > expected_y_tile * TILE_SIZE,
			"Object is not above slope tile after jumping from {0} of {1} tile. Expected to be greater than {2} but got {3}.".format(
			location, slope_type, expected_y_tile * TILE_SIZE, self.obj.y))

	def test_falling_onto_positive_slope(self):
		"""Tests the resolution of collisions with 1-tile positive slopes after falling onto them.
		TODO Remove the assumption about the tile size
		PLEASE NOTE: This test assumes a tile size of 32
		"""
		movement = "straight down"
		slope_type = "positive"

		# Test falling onto a 1-tile positive slope, perfectly aligned (should be completely centered on tile)
		self._assert_slope_resolution((6, 3.5), ("flush with", "centered on"), movement, slope_type)

		# Test falling onto a 1-tile positive slope, bottom-center on the peak (should be at the same x and the peak of the slope)
		self.obj.reset_to_tile(7-self.half_tile_width, 5)
		self._assert_slope_resolution((7-self.half_tile_width, 4), ("centered over right end of", "on peak of"), movement, slope_type)

		# Test falling onto a 1-tile positive slope, bottom-center on the lowest point (should be at the same x and the bottom of the slope)
		self.obj.reset_to_tile(6-self.half_tile_width, 5)
		self._assert_slope_resolution((6-self.half_tile_width, 3), ("centered over left end of", "on bottom of"), movement, slope_type)

	def test_falling_onto_2_tile_positive_slope(self):
		"""Tests the resolution of collisions with 2-tile positive slopes after falling onto them.
		TODO Remove the assumption about the tile size
		PLEASE NOTE: This test assumes a tile size of 32
		"""
		movement = "straight down"
		slope_type = "lower end of two-tile positive"

		# Test falling onto a 2-tile positive slope, perfectly aligned with lower tile (lower tile is 8px tall in the middle)
		self.obj.reset_to_tile(4, 4)
		self._assert_slope_resolution((4, 2+(8.0/TILE_SIZE)), ("flush with", "on middle of lower"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the lower tile's peak (lower tile is 16px tall at its peak)
		self.obj.reset_to_tile(5-self.half_tile_width, 4)
		self._assert_slope_resolution((5-self.half_tile_width, 2+(16.0/TILE_SIZE)), ("centered over right end of", "at peak of lower"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the lower tile's lowest point (lower tile is 0px tall at bottom)
		self.obj.reset_to_tile(4-self.half_tile_width, 4)
		self._assert_slope_resolution((4-self.half_tile_width, 2), ("centered over left end of", "at bottom of lower"), movement, slope_type)

		slope_type = "upper end of two-tile positive"

		# Test falling onto a 2-tile positive slope, perfectly aligned with upper tile (upper tile is 25px tall in the middle)
		self.obj.reset_to_tile(5, 4)
		self._assert_slope_resolution((5, 2+(25.0/TILE_SIZE)), ("flush with", "on middle of upper"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the upper tile's peak (upper tile is 32px tall at its peak)
		self.obj.reset_to_tile(6-self.half_tile_width, 4)
		self._assert_slope_resolution((6-self.half_tile_width, 3), ("centered over right end of", "at peak of upper"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the upper tile's lowest point
		# (upper tile is 17px at bottom, but it is considered to be on the lower tile, which has its peak at 16px)
		self.obj.reset_to_tile(5-self.half_tile_width, 4)
		self._assert_slope_resolution((5-self.half_tile_width, 2+(16.0/TILE_SIZE)), ("centered over left end of", "at bottom of upper"), movement, slope_type)

	def test_falling_onto_negative_slope(self):
		"""Tests the resolution of collisions with 1-tile negative slopes after falling onto them.
		TODO Remove the assumption about the tile size
		PLEASE NOTE: This test assumes a tile size of 32
		"""
		movement = "straight down"
		slope_type = "negative"

		# Test falling onto a 1-tile negative slope, perfectly aligned (should be completely centered on tile)
		self.obj.reset_to_tile(8, 4)
		self._assert_slope_resolution((8, 3.5), ("flush with", "centered on"), movement, slope_type)

		# Test falling onto a 1-tile negative slope, bottom-center on the peak
		self.obj.reset_to_tile(8-self.half_tile_width, 4)
		self._assert_slope_resolution((8-self.half_tile_width, 4), ("centered over right left of", "on peak of"), movement, slope_type)

		# Test falling onto a 1-tile negative slope, bottom-center on the lowest point
		self.obj.reset_to_tile(9-self.half_tile_width, 4)
		self._assert_slope_resolution((9-self.half_tile_width, 3), ("centered over right end of", "on bottom of"), movement, slope_type)

	# TODO 2-tile negative slope tests

	def test_jumping_from_positive_slope(self):
		"""Tests the resolution of jumping from a 1-tile positive slope.
		TODO Remove the assumption about the tile size
		PLEASE NOTE: This test assumes a tile size of 32
		"""
		slope_type = 'positive'

		# Test jumping from a 1-tile positive slope when perfectly aligned
		self.obj.reset_to_tile(6, 4)
		self._assert_slope_jump_resolution(3.5, "center", slope_type)

		# Test jumping from a 1-tile positive slope, bottom-center on peak
		self.obj.reset_to_tile(7-self.half_tile_width, 5)
		self._assert_slope_jump_resolution(4, "right end", slope_type)

		# Test jumping from a 1-tile positive slope, bottom-center on the lowest point
		self.obj.reset_to_tile(6-self.half_tile_width, 5)
		self._assert_slope_jump_resolution(3, "left end", slope_type)

		# Test jumping from a 1-tile positive slope, bottom-center 1 pixel left of the lowest point (we're actually on the 2-tile positive slope)
		# This check ensures that objects do not get stuck when jumping near the seam of two positive slopes
		self.obj.reset_to_tile(5 + (self.half_width * 0.125 / TILE_SIZE), 5)
		self._assert_slope_jump_resolution(3, "1 pixel left of the bottom left (actually on top of upper 2-tile positive slope tile)", slope_type)

	def test_jumping_from_2_tile_positive_slope(self):
		"""Tests the resolution of jumping from a 2-tile positive slope.
		TODO Remove the assumption about the tile size
		PLEASE NOTE: This test assumes a tile size of 32
		"""
		slope_type = 'lower two-tile positive slope'

		# Test jumping from a 2-tile positive slope, perfectly aligned with lower tile
		self.obj.reset_to_tile(4, 3)
		self._assert_slope_jump_resolution(2+(8.0/TILE_SIZE), "center", slope_type)

		# Test jumping from a 2-tile positive slope, bottom-center on the lower tile's peak
		self.obj.reset_to_tile(5-self.half_tile_width, 3)
		self._assert_slope_jump_resolution(2+(17.0/TILE_SIZE), "peak", slope_type)

		# Test jumping from a 2-tile positive slope, bottom-center on the lower tile's lowest point
		self.obj.reset_to_tile(4-self.half_tile_width, 3)
		self._assert_slope_jump_resolution(2, "bottom", slope_type)

		# Test jumping from a 2-tile positive slope, bottom-center 1 pixel left of the middle (we're actually on the 3-tile positive slope)
		# This check ensures that objects do not get stuck when jumping near the seam of two positive slopes
		self.obj.reset_to_tile((4.0-(self.half_width + 2) / TILE_SIZE), 3)
		self._assert_slope_jump_resolution(2, "1 pixel left of the middle (left side is actually on top of upper 3-tile positive slope tile)", slope_type)

		# Begin testing jumps from the upper tile of a 2-tile positive slope
		slope_type = 'upper two-tile positive slope'

		# Test jumping from a 2-tile positive slope, perfectly aligned with upper tile
		self.obj.reset_to_tile(5, 3)
		self._assert_slope_jump_resolution(2+(25.0/TILE_SIZE), "center", slope_type)

		# Test jumping from a 2-tile positive slope, bottom-center on the upper tile's peak
		self.obj.reset_to_tile(6-self.half_tile_width, 3)
		self._assert_slope_jump_resolution(3, "peak", slope_type)

		# Test jumping from a 2-tile positive slope, bottom-center on the upper tile's lowest point
		self.obj.reset_to_tile(5-self.half_tile_width, 3)
		self._assert_slope_jump_resolution(2+(17.0/TILE_SIZE), "bottom", slope_type)

		# Test jumping from a 2-tile positive slope, bottom-center 1 pixel left of the middle (we're actually on the lower tile)
		# This check ensures that objects do not get stuck when jumping near the seam of two slopes
		self.obj.reset_to_tile(5.0 - (self.half_width + 2)/TILE_SIZE, 3)
		self._assert_slope_jump_resolution(2+(17.0/TILE_SIZE), "1 pixel left of the middle (left side is actually on top of lower 2-tile positive slope tile)", slope_type)
