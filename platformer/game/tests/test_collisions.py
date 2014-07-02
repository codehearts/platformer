from game.settings.general_settings import TILE_SIZE, FRAME_LENGTH, FPS
from game.physical_objects.physical_object import PhysicalObject
from game.tiles import TileMap, Tileset
from game.tiles.tileset import TilesetImage, TilesetConfig
from util.tileset import get_testing_tileset
from util.image import dummy_image
import unittest

class TestCollisions(unittest.TestCase):
	"""Tests that object collisions are resolved as expected."""

	def _check_object_reaction(self, reset_to, expected_tiles, velocity):
		"""Asserts that the object is resolved to the correct coordinates.

		Args:
			reset_to (tuple of float): The tiles to reset the object to.
			expected_tiles (tuple of float): The exact tiles that the object should be resolved to.
			velocity (tuple of float): The velocities the object should be reset to. This is used for determining
			                           which direction the object came from during collision resolution.
		"""
		# Move the object to our initial tile (move_to() will automatically resolve collisions)
		x, y = reset_to[0] * TILE_SIZE, reset_to[1] * TILE_SIZE
		expected_x, expected_y = expected_tiles[0] * TILE_SIZE, expected_tiles[1] * TILE_SIZE

		self.obj.reset_to(x, y) # Reseting will reset the velocity
		self.obj.target_speed, self.obj.velocity_y = velocity # The target speed is the horizontal velocity that the object is approaching
		self.obj.update(FRAME_LENGTH)

		self.assertEqual(expected_x, self.obj.x,
			"Failed to resolve horizontal component of collision with x velocity "+str(self.obj.velocity_x)+
			", expected "+str(expected_x)+" but got "+str(self.obj.x))

		self.assertEqual(expected_y, self.obj.y,
			"Failed to resolve vertical component of collision with y velocity "+str(self.obj.velocity_y)+
			", expected "+str(expected_y)+" but got "+str(self.obj.y))

	def test_object_collision_handling(self):
		"""Tests a physical object's responses to colliding with the environment in different ways."""
		collision_map = [
			[ 2, 2, 2, 2],
			[ 2,00,00, 2],
			[ 2,00,00, 2],
			[ 2, 2, 2, 2]
		]
		collision_level = TileMap(collision_map, get_testing_tileset(2,2))

		self.obj = PhysicalObject(collision_level.tiles, dummy_image(TILE_SIZE, TILE_SIZE), TILE_SIZE*2, TILE_SIZE, mass=0)
		offset = 4.0 / TILE_SIZE

		# Partially embedded in the left wall, moving left and down
		self._check_object_reaction(reset_to=(1 - offset, 1), expected_tiles=(1, 1), velocity=(-1, -1))

		# Partially embedded in the right wall, moving right and down
		self._check_object_reaction(reset_to=(2 + offset, 1), expected_tiles=(2, 1), velocity=(1, -1))

		# Partially embedded in the floor, colliding with 1 tile, moving down
		self._check_object_reaction(reset_to=(1, 1 - offset), expected_tiles=(1, 1), velocity=(0, -1))

		# Partially embedded in the floor, colliding with 2 tiles, moving down
		self._check_object_reaction(reset_to=(1.5, 1 - offset), expected_tiles=(1.5, 1), velocity=(0, -1))

		# Partially embedded in the left wall and floor, moving left and down
		self._check_object_reaction(reset_to=(1 - offset, 1 - offset), expected_tiles=(1, 1), velocity=(-1, -1))

		# Partially embedded in the right wall and floor, moving right and down
		self._check_object_reaction(reset_to=(2 + offset, 1 - offset), expected_tiles=(2, 1), velocity=(1, -1))

		# Partially embedded in the ceiling, moving up
		self._check_object_reaction(reset_to=(1, 2 + offset), expected_tiles=(1, 2), velocity=(0, 1))

		# Partially embedded in the left wall and ceiling, moving left and uo
		self._check_object_reaction(reset_to=(1 - offset, 2 + offset), expected_tiles=(1, 2), velocity=(-1, 1))

		# Partially embedded in the right wall and ceiling, moving right and up
		self._check_object_reaction(reset_to=(2 + offset, 2 + offset), expected_tiles=(2, 2), velocity=(1, 1))



	def _simulate_time(self, seconds, update_object):
		"""Simulates time by calling the given update function every frame for the given amount of time."""
		map(lambda x: update_object.update(FRAME_LENGTH), xrange(int(FPS * seconds)))

	def _assert_slope_resolution(self, expected_tiles, locations, movement, onto):
		"""Asserts that the object has resolved to the expected coordinates on the slope tile.

		Args:
			expected_tiles (tuple of float): The expected tile coordinates of the object after resolution.
			locations (tuple of str): A description of the expected x and y locations on the slope.
			movement (str): A description of the object's movement onto the slope.
			onto (str): A description of the tile the object has moved onto.
		"""
		self.assertEqual(expected_tiles[0]*TILE_SIZE, self.obj.x,
			"Object's x position is not {0} tile after moving {1} onto {2} slope. Expected {3} but got {4}.".format(
			locations[0], movement, onto, expected_tiles[0]*TILE_SIZE, self.obj.x))
		self.assertEqual(expected_tiles[1]*TILE_SIZE, self.obj.y,
			"Object's y position is not {0} tile after moving {1} onto {2} slope. Expected {3} but got {4}.".format(
			locations[1], movement, onto, expected_tiles[1]*TILE_SIZE, self.obj.y))

	def test_slope_collision_handling(self):
		"""Tests the resolution of collisions with slopes tiles.
		TODO: Remove the assumption about the tile size
		PLEASE NOTE: This test assumes a tile size of 32
		"""
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
		half_width= float(self.obj.half_width)
		half_tile_width = half_width / TILE_SIZE

		# Positive slope tests

		# Test falling onto a 1-tile positive slope, perfectly aligned
		movement = "straight down"
		slope_type = "positive"

		self._simulate_time(1, self.obj)
		# The object should have landed centered on the tile
		self._assert_slope_resolution((6, 3.5), ("flush with", "centered on"), movement, slope_type)

		# Test falling onto a 1-tile positive slope, bottom-center on the peak
		self.obj.reset_to_tile(7-(half_width/TILE_SIZE), 5)
		self._simulate_time(1, self.obj)
		# The object should be at the same x-coordinate, and at the peak of the slope
		self._assert_slope_resolution((7-half_tile_width, 4), ("centered over right end of", "on peak of"), movement, slope_type)

		# Test falling onto a 1-tile positive slope, bottom-center on the lowest point
		self.obj.reset_to_tile(6-(half_width/TILE_SIZE), 5)
		self._simulate_time(1, self.obj)
		# The object should be at the same x-coordinate, and at the bottom of the slope
		self._assert_slope_resolution((6-half_tile_width, 3), ("centered over left end of", "on bottom of"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, perfectly aligned with lower tile
		movement = "straight down"
		slope_type = "lower end of two-tile positive"

		self.obj.reset_to_tile(4, 4)
		self._simulate_time(1, self.obj)
		# The height of the lower tile in the middle is 8 pixels
		self._assert_slope_resolution((4, 2+(8.0/TILE_SIZE)), ("flush with", "on middle of lower"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the lower tile's peak
		self.obj.reset_to_tile(5-(half_width/TILE_SIZE), 4)
		self._simulate_time(1, self.obj)
		# The lower tile's peak is 16 pixels
		self._assert_slope_resolution((5-half_tile_width, 2+(16.0/TILE_SIZE)), ("centered over right end of", "at peak of lower"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the lower tile's lowest point
		self.obj.reset_to_tile(4-(half_width/TILE_SIZE), 4)
		self._simulate_time(1, self.obj)
		# The lower tile's lowest point is 0
		self._assert_slope_resolution((4-half_tile_width, 2), ("centered over left end of", "at bottom of lower"), movement, slope_type)

		# Begin testing on the upper tile
		slope_type = "upper end of two-tile positive"

		# Test falling onto a 2-tile positive slope, perfectly aligned with upper tile
		self.obj.reset_to_tile(5, 4)
		self._simulate_time(1, self.obj)
		# The height of the upper tile in the middle is 25 pixels
		self._assert_slope_resolution((5, 2+(25.0/TILE_SIZE)), ("flush with", "on middle of upper"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the upper tile's peak
		self.obj.reset_to_tile(6-(half_width/TILE_SIZE), 4)
		self._simulate_time(1, self.obj)
		# The upper tile's peak is 32 pixels
		self._assert_slope_resolution((6-half_tile_width, 3), ("centered over right end of", "at peak of upper"), movement, slope_type)

		# Test falling onto a 2-tile positive slope, bottom-center on the upper tile's lowest point
		self.obj.reset_to_tile(5-(half_width/TILE_SIZE), 4)
		self._simulate_time(1, self.obj)
		# The second tile's lowest point is 17, but it is considered to be on top of the first tile, which ends at 16
		self._assert_slope_resolution((5-half_tile_width, 2+(16.0/TILE_SIZE)), ("centered over left end of", "at bottom of upper"), movement, slope_type)



		# Negative slope tests

		# Test falling onto a 1-tile negative slope, perfectly aligned

		self.obj.reset_to_tile(8, 4)
		self._simulate_time(1, self.obj)

		# The object should have landed centered on the tile
		self.assertEqual(8*TILE_SIZE, self.obj.x,
			"Object's x position is not flush with tile after falling straight down onto negative slope.")
		self.assertEqual(3.5*TILE_SIZE, self.obj.y,
			"Object's y position is not centered on tile after falling straight down onto negative slope.")



		# Test falling onto a 1-tile leftward slope, bottom-center on the peak

		self.obj.reset_to_tile(8-(half_width/TILE_SIZE), 4)

		# Simulate 1 second of game time
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be at the same x-coordinate, and at the peak of the slope
		self.assertEqual(util.tile_to_coordinate(8-(half_width/TILE_SIZE), 4), self.obj.get_coordinates())



		# Test falling onto a 1-tile leftward slope, bottom-center on the lowest point

		self.obj.reset_to_tile(9-(half_width/TILE_SIZE), 4)

		# Simulate 1 second of game time
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be at the same x-coordinate, and at the bottom of the slope
		self.assertEqual(util.tile_to_coordinate(9-(half_width/TILE_SIZE), 3), self.obj.get_coordinates())



		# Slope jump tests



		# Test jumping from a 1-tile rightward slope when perfectly aligned

		self.obj.reset_to_tile(6, 4)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(3.5*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 1-tile rightward slope, bottom-center on peak

		self.obj.reset_to_tile(7-(half_width/TILE_SIZE), 5)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(4*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 1-tile rightward slope, bottom-center on the lowest point

		self.obj.reset_to_tile(6-(half_width/TILE_SIZE), 5)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(3*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 1-tile rightward slope, bottom-center 1 pixel left of the lowest point (we're actually on the 2-tile slope)
		# This check ensures that we do not get stuck when jumping near the seam of two slopes

		self.obj.reset_to_tile(5 + (half_width * 0.125 / TILE_SIZE), 5)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(3*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, perfectly aligned with first tile

		self.obj.reset_to_tile(4, 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue((2+(8/TILE_SIZE))*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, bottom-center on the first tile's peak

		self.obj.reset_to_tile(5-(half_width/TILE_SIZE), 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue((2+(17/TILE_SIZE))*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, bottom-center on the first tile's lowest point

		self.obj.reset_to_tile(4-(half_width/TILE_SIZE), 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(2*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, perfectly aligned with second tile

		self.obj.reset_to_tile(5, 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue((2+(25/TILE_SIZE))*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, bottom-center on the second tile's peak

		self.obj.reset_to_tile(6-(half_width/TILE_SIZE), 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(3*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, bottom-center on the second tile's lowest point

		self.obj.reset_to_tile(5-(half_width/TILE_SIZE), 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue((2+(17/TILE_SIZE))*TILE_SIZE < self.obj.get_coordinates()[1])



		# Test jumping from a 2-tile rightward slope, bottom-center 1 pixel left of the middle (we're actually on the 3-tile slope)
		# This check ensures that we do not get stuck when jumping near the seam of two slopes

		self.obj.reset_to_tile((4-(half_width + 2) / TILE_SIZE), 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue(2*TILE_SIZE < self.obj.get_coordinates()[1], 'Jumping at slope seams failed')



		# Test jumping from a 2-tile rightward slope, bottom-center 1 pixel left of the middle (we're actually on the first tile)
		# This check ensures that we do not get stuck when jumping near the seam of two slopes

		self.obj.reset_to_tile(5 - (half_width + 2)/TILE_SIZE, 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		self.obj.jump()

		# Simulate a quarter of a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be above where it would be if it were resting on the slope
		self.assertTrue((2+(17/TILE_SIZE))*TILE_SIZE < self.obj.get_coordinates()[1], 'Jumping at slope seams failed')



		# Test walking up a 2-tile rightward slope until we're at the top of the first, but not on the second
		# This check ensures that we ascend rightward slopes smoothly

		self.obj.reset_to_tile(4, 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move right up the slope until our hitbox overlaps the second tile
		self.obj.go_to_x(5*TILE_SIZE - 1)

		# Simulate a second of game time to let the object move
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position appropriate for its location on the slope
		self.assertTrue(2.5*TILE_SIZE != self.obj.get_coordinates()[1], 'Ascending 2-tile rightward slopes failed')



		# Test walking off a floor down onto a 1-tile leftward slope until our center is over the slope
		# This check ensures that we begin to descend leftward slopes smoothly

		self.obj.reset_to_tile(7, 8)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move right up the slope until our hitbox overlaps the second tile
		self.obj.go_to_x(8*TILE_SIZE - 2)

		# Simulate a second of game time to let the object move
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position appropriate for its location on the slope
		self.assertTrue(8*TILE_SIZE != self.obj.get_coordinates()[1], 'Descending leftward slopes failed')



		# Test walking down two 1-tile rightward slopes until we're almost centered over the first one
		# This check ensures that we descend rightward slopes smoothly

		self.obj.reset_to_tile(6, 8)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move left down the slope until our hitbox overlaps the first tile
		self.obj.go_to_x(5*TILE_SIZE + 2)

		# Simulate a second of game time to let the object move
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position appropriate for its location on the slope
		self.assertTrue(7*TILE_SIZE != self.obj.get_coordinates()[1], 'Descending rightward slopes failed')



		# Test walking down two 1-tile rightward slopes until we're almost centered over the second one
		# This check ensures that we descend leftward slopes smoothly

		self.obj.reset_to_tile(8, 8)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move right down the slope until our hitbox overlaps the second tile
		self.obj.go_to_x(9*TILE_SIZE - 2)

		# Simulate a second of game time to let the object move
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position appropriate for its location on the slope
		self.assertTrue(7*TILE_SIZE != self.obj.get_coordinates()[1], 'Descending leftward slopes failed')



		# Test placing the object on a 2-tile leftward slope so they overlap both tiles but their center is over the second one
		# This check ensures that we move smoothly on 2-tile leftward slopes

		self.obj.reset_to_tile(9.75, 3)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position appropriate for its location on the slope
		# 17 is the height of the lowest point on the first tile
		self.assertTrue(2*TILE_SIZE + 17 != self.obj.get_coordinates()[1], 'Movement on 2-tile leftward slopes failed')



		# Test behavoir at the bottom of rightward slopes suspended in mid air
		# This check ensures that slopes have the same "standing area" as a full tile has

		self.obj.reset_to_tile(4 + (1/TILE_SIZE), 6)

		# Simulate a quarter of a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be standing on the slope tile
		self.assertTrue(6*TILE_SIZE == self.obj.get_coordinates()[1], 'Standing at the bottom of suspended rightward slopes failed')

		self.obj.reset_to_tile(4, 6)

		# Simulate a quarter of a second of game time to fall
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be below the slope tile, as it should be falling
		self.assertTrue(6*TILE_SIZE > self.obj.get_coordinates()[1], 'Falling off the bottom of suspended rightward slopes failed')



		# Test behavoir at the bottom of leftward slopes suspended in mid air
		# This check ensures that slopes have the same "standing area" as a full tile has

		self.obj.reset_to_tile(10 - (1/TILE_SIZE), 6)

		# Simulate a quarter of a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be standing on the slope tile
		self.assertTrue(6*TILE_SIZE == self.obj.get_coordinates()[1], 'Standing at the bottom of suspended leftward slopes failed')

		self.obj.reset_to_tile(10, 6)

		# Simulate a quarter of a second of game time to fall
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should be below the slope tile, as it should be falling
		self.assertTrue(6*TILE_SIZE > self.obj.get_coordinates()[1], 'Falling off the bottom of suspended leftward slopes failed')



		# Test falling off a rightward slope directly into the empty space of a leftward slope tile below it
		# This check ensures that we are registered as being aerial and fall onto the slope instead of "snapping" onto it

		self.obj.reset_to_tile(5, 7)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move left down the slope until we fall off onto the leftward slope
		self.obj.go_to_x(4*TILE_SIZE)

		# Simulate a quarter of a second of game time to let the object move off the slope and begin falling
		for i in xrange(int(general_settings.FPS * 0.25)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position above the leftward slope, but below the rightward slope
		y_pos = self.obj.get_coordinates()[1]
		self.assertTrue(5.25*TILE_SIZE < y_pos and 6*TILE_SIZE > y_pos, 'Falling from rightward to lower leftward slope below failed')



		# Test falling off a rightward slope directly into the empty space of a rightward slope tile at the same y-coordinate
		# This check ensures that we are registered as being aerial and fall onto the slope instead of "snapping" onto it

		self.obj.reset_to_tile(3, 6)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move left up the slope until we fall off onto the rightward slope
		self.obj.go_to_x(2*TILE_SIZE)

		# Simulate a fifteenth of a second of game time to let the object move off the slope and begin falling
		for i in xrange(int(general_settings.FPS * 0.15)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position above the second slope, but below the first slope
		y_pos = self.obj.get_coordinates()[1]
		self.assertTrue(5.5*TILE_SIZE < y_pos and 6*TILE_SIZE > y_pos, 'Falling from leftward to lower leftward slope (same y-pos) failed')



		# Test falling off a leftward slope directly into the empty space of a rightward slope tile below it
		# This check ensures that we are registered as being aerial and fall onto the slope instead of "snapping" onto it

		self.obj.reset_to_tile(9, 7)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move right down the slope until we fall off onto the rightward slope
		self.obj.go_to_x(12*TILE_SIZE)

		# Simulate half a second of game time to let the object move off the slope and begin falling
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position above the rightward slope, but below the leftward slope
		y_pos = self.obj.get_coordinates()[1]
		self.assertTrue(5.25*TILE_SIZE < y_pos and 6*TILE_SIZE > y_pos, 'Falling from leftward to lower rightward slope below failed')



		# Test falling off a lefward slope directly into the empty space of a leftward slope tile at the same y-coordinate
		# This check ensures that we are registered as being aerial and fall onto the slope instead of "snapping" onto it

		self.obj.reset_to_tile(11, 6)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move right up the slope until we fall off onto the leftward slope
		self.obj.go_to_x(12*TILE_SIZE)

		# Simulate around a third of a second of game time to let the object move off the slope and begin falling
		for i in xrange(int(general_settings.FPS * 0.3)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should resolve to a position above the second slope, but below the first slope
		y_pos = self.obj.get_coordinates()[1]
		self.assertTrue(5.5*TILE_SIZE < y_pos and 6*TILE_SIZE > y_pos, 'Falling from leftward to lower leftward slope (same y-pos) failed')



		# Test jumping into the bottom of a rightward slope, horizontally centered with it

		self.obj.reset_to_tile(15, 1)

		self.obj.jump()

		# Simulate half a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not be above the slope tile
		self.assertTrue(2*TILE_SIZE > self.obj.get_coordinates()[1], 'Centered collision with bottom of rightward slope failed')



		# Test jumping into the bottom of a rightward slope, barely touching its left side

		self.obj.reset_to_tile(14 + (1/TILE_SIZE), 1)

		self.obj.jump()

		# Simulate half a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not be above the slope tile
		self.assertTrue(2*TILE_SIZE > self.obj.get_coordinates()[1], 'Left-side collision with bottom of rightward slope failed')



		# Test jumping into the bottom of a rightward slope, barely touching its right side

		self.obj.reset_to_tile(16 - (1/TILE_SIZE), 1)

		self.obj.jump()

		# Simulate half a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not be above the slope tile
		self.assertTrue(2*TILE_SIZE > self.obj.get_coordinates()[1], 'Right-side collision with bottom of rightward slope failed')



		# Test jumping into the bottom of a leftward slope, horizontally centered with it

		self.obj.reset_to_tile(17, 1)

		self.obj.jump()

		# Simulate half a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not be above the slope tile
		self.assertTrue(2*TILE_SIZE > self.obj.get_coordinates()[1], 'Centered collision with bottom of leftward slope failed')



		# Test jumping into the bottom of a leftward slope, barely touching its left side

		self.obj.reset_to_tile(16 + (1/TILE_SIZE), 1)

		self.obj.jump()

		# Simulate half a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not be above the slope tile
		self.assertTrue(2*TILE_SIZE > self.obj.get_coordinates()[1], 'Left-side collision with bottom of leftward slope failed')



		# Test jumping into the bottom of a leftward slope, barely touching its right side

		self.obj.reset_to_tile(18 - (1/TILE_SIZE), 1)

		self.obj.jump()

		# Simulate half a second of game time to let the object jump up
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not be above the slope tile
		self.assertTrue(2*TILE_SIZE > self.obj.get_coordinates()[1], 'Right-side collision with bottom of leftward slope failed')



		# Test walking into a rightward slope from its taller end

		self.obj.reset_to_tile(7, 7)

		# Try to move into the slope's taller end
		self.obj.go_to_x(6)

		# Simulate a tenth of a second of game time to let the object collide with the slope's taller end
		for i in xrange(int(general_settings.FPS * 0.1)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not pass through the slope
		self.assertTrue(7*TILE_SIZE == self.obj.get_coordinates()[0], 'Collision with rightward slope at tall end failed')



		# Test walking into a leftward slope from its taller end

		self.obj.reset_to_tile(7, 7)

		# Try to move into the slope's taller end
		self.obj.go_to_x(8)

		# Simulate a tenth of a second of game time to let the object collide with the slope's taller end
		for i in xrange(int(general_settings.FPS * 0.1)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# The object should not pass through the slope
		self.assertTrue(7*TILE_SIZE == self.obj.get_coordinates()[0], 'Collision with leftward slope at tall end failed')



		# Test walking off the tall end of a rightward slope over another slope
		# This ensures that we stand on the rightward slope until our hitbox would not overlap the tile when on the second slope

		self.obj.reset_to_tile(12, 6)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move our bottom-center hitbox off the rightward slope's tall end and over the next slope
		self.obj.go_to_x(13*TILE_SIZE - 1)

		# Simulate half a second of game time to let the object move
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should still be standing on the tall end, because if we were placed on the second slope we'd intersect the first slope
		self.assertTrue(6*TILE_SIZE == self.obj.get_coordinates()[1], 'Standing on tall end of rightward slope over rightward slope failed')



		# Test falling on the tall end of a rightward slope over another rightward slope
		# This ensures that we stand on the tall end of the rightward slope

		self.obj.reset_to_tile(18 - (1 / general_settings.TILE_SIZE_FLOAT), 6)

		# Simulate half a second of game time to allow a resolution
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should still be standing on the tall end, because if we were placed on the second slope we'd intersect the first slope
		self.assertTrue(6*TILE_SIZE == self.obj.get_coordinates()[1], 'Falling on tall end of rightward slope over rightward slope failed')



		# Test walking off the tall end of a leftward slope over another slope
		# This ensures that we stand on the leftward slope until our hitbox would not overlap the tile when on the second slope

		self.obj.reset_to_tile(2, 6)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move our bottom-center hitbox off the leftward slope's tall end and over the next slope
		self.obj.go_to_x(2*TILE_SIZE - half_width - 1)

		# Simulate half a second of game time to let the object move
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should still be standing on the tall end, because if we were placed on the second slope we'd intersect the first slope
		self.assertTrue(6*TILE_SIZE == self.obj.get_coordinates()[1], 'Standing on tall end of leftward slope over leftward slope failed')



		# Test falling on the tall end of a leftward slope over another leftward slope
		# This ensures that we stand on the tall end of the leftward slope

		self.obj.reset_to_tile(19 + (1 / general_settings.TILE_SIZE_FLOAT), 6)

		# Simulate half a second of game time to allow a resolution
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should still be standing on the tall end, because if we were placed on the first slope we'd intersect the second slope
		# @TODO Could this issue be caused by the fact that the slope is collidable?
		self.assertTrue(6*TILE_SIZE == self.obj.get_coordinates()[1], 'Falling on tall end of leftward slope over leftward slope failed')



		# Test walking into the tall side of a rightward slope while on a rightward slope

		self.obj.reset_to_tile(14, 6)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move past the slope's tall end
		self.obj.go_to_x(11*TILE_SIZE)

		# Simulate half a second of game time to let the object move
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should have been stopped by the tall end of the tile
		self.assertTrue(13*TILE_SIZE == self.obj.get_coordinates()[0], 'Walking into tall end of rightward slope from slope failed')



		# Test walking into the tall side of a leftward slope while on a leftward slope

		self.obj.reset_to_tile(0, 6)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Move past the slope's tall end
		self.obj.go_to_x(2*TILE_SIZE)

		# Simulate half a second of game time to let the object move
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should have been stopped by the tall end of the tile
		self.assertTrue(TILE_SIZE == self.obj.get_coordinates()[0], 'Walking into tall end of leftward slope from slope failed')



		# Test walking into a wall while walking down a rightward slope

		self.obj.reset_to_tile(15, 8)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Attempt to walk past the wall
		self.obj.go_to_x(12*TILE_SIZE)

		# Simulate a second of game time to let the object move
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should have been stopped by the wall
		self.assertTrue(14*TILE_SIZE == self.obj.get_coordinates()[0], 'Walking into wall while going down rightward slope failed')



		# Test walking into a wall while walking down a leftward slope

		self.obj.reset_to_tile(16, 8)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# Attempt to walk past the wall
		self.obj.go_to_x(19*TILE_SIZE)

		# Simulate a second of game time to let the object move
		for i in xrange(int(general_settings.FPS)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should have been stopped by the wall
		self.assertTrue(17*TILE_SIZE == self.obj.get_coordinates()[0], 'Walking into wall while going down leftward slope failed')



		# Test standing on a wall next to a rightward slope

		self.obj.reset_to_tile(13.5, 8.5)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should be standing on the wall
		self.assertTrue(8*TILE_SIZE == self.obj.get_coordinates()[1], 'Standing on wall next to rightward slope failed')



		# Test standing on a wall next to a leftward slope

		self.obj.reset_to_tile(17.5, 8.5)

		# Simulate half a second of game time to land on the tile
		for i in xrange(int(general_settings.FPS * 0.5)):
			self.obj.update(general_settings.FRAME_LENGTH)

		# We should be standing on the wall
		self.assertTrue(8*TILE_SIZE == self.obj.get_coordinates()[1], 'Standing on wall next to leftward slope failed')

		# @TODO Test ceiling slopes
		# @TODO Write better "top of slope over slope of same direction" tests. Top of rightward next to rightward fails
		# @TODO Test 2-tile tall hitbox moving into the lower edge of a rightward slope while on ground
		# @TODO Test 2-tile tall hitbox moving into the lower edge of a rightward slope while on a leftward slope
		# @TODO Test 2-tile tall hitbox moving into the lower edge of a leftward slope while on ground
		# @TODO Test 2-tile tall hitbox moving into the lower edge of a leftward slope while on a rightward slope



	## Tests speculative collision detection on high velocity objects
	#def test_speculative_object_collision_handling(self):
		#"""
		#PLEASE NOTE: This test assumes a gravity of 9.8, an fps of 120, and a tile size of 32
		#"""


		## speculative_map_2map is 1000x1000 and double-U-shaped
		#speculative_map	 = [[i for i in [2]+[0]+[2]+[0]*994+[3]+[0]+[3]]]*1000
		#speculative_map[997] = [i for i in [2]+[0]+[1]*996+[0]+[3]]
		#speculative_map[998] = [i for i in [2]+[0]*998+[3]]
		#speculative_map[999] = [1]*1000

		## speculative_map_2 is 1000x1000 with a single tile in the center
		#speculative_map_2 = [[0] * 1000 for i in xrange(1000)]
		#speculative_map_2[499][499] = 1

		#speculative_level = load.Stage(demo_settings.TILE_DATA, speculative_map)
		#speculative_level_2 = load.Stage(demo_settings.TILE_DATA, speculative_map_2)



		## Test colliding against the ground

		## Load the heavy test object
		#self.obj = load.single_self.obj('test_object_5', 499, 100, speculative_level.get_tiles())

		## Simulate 5 seconds of game time
		#for i in xrange(int(general_settings.FPS * 5)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## If the object is not on top of the upper row of blocks by this point,
		## the speculation failed and they've gone clean through the tiles
		#self.assertEqual(general_settings.TILE_SIZE*3, self.obj.get_coordinates()[1])



		## Reset the self.obj to test colliding against the left wall

		#self.obj.reset_to_tile(499, 999)
		#self.obj.set_velocity(-50000, 0) # Moving left very fast, but not down (yet; gravity will take care of that)

		## Simulate half a second of game time
		#for i in xrange(int(general_settings.FPS * 0.5)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## The object should have hit the wall by this point, but not the ground
		#self.assertEqual(general_settings.TILE_SIZE*3, self.obj.get_coordinates()[0])



		## Reset the self.obj to test colliding against the right wall

		#self.obj.reset_to_tile(499, 999)
		#self.obj.set_velocity(50000, 0) # Moving left very fast, but not down (yet; gravity will take care of that)

		## Simulate half a second of game time
		#for i in xrange(int(general_settings.FPS * 0.5)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## The object should have hit the wall by this point, but not the ground
		#self.assertEqual(997*general_settings.TILE_SIZE-self.obj.get_width(), self.obj.get_coordinates()[0])



		## Reset the self.obj to test a 45 degree collision with the bottom right corner of the stage

		#self.obj.reset_to_tile(3, 996)

		## For this test we'll want clean, equal numbers for the velocities and no accelerations
		#self.obj.set_velocity(20000, -20000)
		#self.obj.set_acceleration(1, 0) # We're not using acceleration because it's handled differently on the x-axis

		## Simulate 3 seconds of game time (around 2.5 is enough time for the object to reach (999,0))
		#for i in xrange(int(general_settings.FPS * 3)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## The object should have resolved to (996,3) instead of passing through the corner
		#self.assertEqual(util.tile_to_coordinate(996, 3), self.obj.get_coordinates())



		## Reset the self.obj to test a 45 degree collision with the bottom left corner of the stage

		#self.obj.reset_to_tile(996, 996)

		## For this test we'll want clean, equal numbers for the velocities and no accelerations
		#self.obj.set_velocity(-20000, -20000)
		#self.obj.set_acceleration(1, 0)

		## Simulate 3 seconds of game time (around 2.5 is enough time for the object to reach (0,0))
		#for i in xrange(int(general_settings.FPS * 3)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## The object should have resolved to (3,3) instead of passing through the corner
		#self.assertEqual(util.tile_to_coordinate(3, 3), self.obj.get_coordinates())



		## Test collisions with a single obstacle in the path

		#"""
		#PLEASE NOTE: These tests will fail if the object's instantaneous velocity is greater than 3840
		#"""

		## Reload a self.obj on a new map
		#self.obj = load.single_self.obj('test_object_5', -1, 999, speculative_level_2.get_tiles())



		## Reset the self.obj to test a 45 degree collision with the top left corner of a block in its path

		## For this test we'll want clean, equal numbers for the velocities and no acceleration
		## 3000 is under 32*120, so it should be a safe velocity
		#self.obj.set_velocity(3600, -3600)
		#self.obj.set_acceleration(1, 0)

		## Simulate 6 seconds of game time (enough time for the object to pass (499,499))
		#for i in xrange(int(general_settings.FPS * 6)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## The object should have resolved to the left side of the block, instead of passing through the block
		#self.assertEqual(499*general_settings.TILE_SIZE-self.obj.get_width(), self.obj.get_coordinates()[0])

		## It should also have a horizontal velocity of 0 due to the collision, but maintains Vy
		#self.assertEqual(0, self.obj.get_velocity()[0])
		#self.assertTrue(self.obj.get_velocity()[1] < 0)



		## Reset the self.obj to test a 45 degree collision with the left side of a block in its path

		#self.obj.reset_to_tile(-2, 999)

		## For this test we'll want clean, equal numbers for the velocities and no acceleration
		## 3000 is under 32*120, so it should be a safe velocity
		#self.obj.set_velocity(3600, -3600)
		#self.obj.set_acceleration(1, 0)

		## Simulate 6 seconds of game time (enough time for the object to reach (499,499))
		#for i in xrange(int(general_settings.FPS * 6)):
			#self.obj.update(general_settings.FRAME_LENGTH)

		## The object should have resolved to the left side of the block, instead of passing through the block
		#self.assertEqual(499*general_settings.TILE_SIZE-self.obj.get_width(), self.obj.get_coordinates()[0])

		## It should also have a horizontal velocity of 0 due to the collision, but maintains Vy
		#self.assertEqual(0, self.obj.get_velocity()[0])
		#self.assertTrue(self.obj.get_velocity()[1] < 0)
