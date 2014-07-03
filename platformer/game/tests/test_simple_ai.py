from game.settings.general_settings import TILE_SIZE
from game.physical_objects.simpleai import SimpleAI
from game.tiles import TileMap
from util.tileset import get_testing_tileset
from util import dummy_image, simulate_time
import unittest

class TestSimpleAI(unittest.TestCase):
	"""Ensures that the simple AI behaves as expected."""

	def test_horizontal_movement(self):
		"""Tests the horizontal movement of simple AI."""
		flat_map = [[2] * 100] # flat_map is 100 tiles of basic tile
		flat_level = TileMap(flat_map, get_testing_tileset(2, 2))

		self.ai = SimpleAI(flat_level.tiles, dummy_image(TILE_SIZE, TILE_SIZE), 0, TILE_SIZE, mass=100)

		# Tell it to move right to 50
		self.ai.go_to_x(50)
		simulate_time(1, self.ai)
		self.assertEqual(50, self.ai.x, "Simple AI did not move right to requested x coordinate.")
		self.assertEqual(TILE_SIZE, self.ai.y, "Simple AI is not at expected y coordinate after moving right.")

		# Tell it to move left to 25
		self.ai.go_to_x(25)
		simulate_time(1, self.ai)
		self.assertEqual(25, self.ai.x, "Simple AI did not move left to requested x coordinate.")
		self.assertEqual(TILE_SIZE, self.ai.y, "Simple AI is not at expected y coordinate after moving left.")

		# Tell it to move right to 100
		self.ai.go_to_x(100)
		simulate_time(0.1, self.ai)
		# The object shouldn't be where we told it to go yet, but it should be moving in that direction
		self.assertTrue(25 < self.ai.x, "Simple AI did not begin moving right to requested x coordinate after 0.1 seconds.")
		self.assertTrue(100 > self.ai.x, "Simple AI is already at or beyond requested x coordinate after moving right for 0.1 seconds.")

		# Interupt the object to tell it to instead move to tile 5 (at this point it's still moving to 100)
		self.ai.go_to_tile_x(5)
		simulate_time(2, self.ai)
		self.assertEqual(5*TILE_SIZE, self.ai.x, "Simple AI did not move right to requested x tile coordinate.")
		self.assertEqual(TILE_SIZE, self.ai.y, "Simple AI is not at expected y coordinate after moving right.")

		# Tell it to move left to tile 2
		self.ai.go_to_tile_x(2)
		simulate_time(1, self.ai)
		self.assertEqual(2*TILE_SIZE, self.ai.x, "Simple AI did not move left to requested x tile coordinate.")
		self.assertEqual(TILE_SIZE, self.ai.y, "Simple AI is not at expected y coordinate after moving left.")

		# Tell it to move right to tile 50
		self.ai.go_to_tile_x(50)
		simulate_time(0.1, self.ai)
		# The object shouldn't be where we told it to go yet, but it should be moving in that direction
		self.assertTrue(2*TILE_SIZE < self.ai.x, "Simple AI did not begin moving right to requested x tile coordinate after 0.1 seconds.")
		self.assertTrue(50*TILE_SIZE > self.ai.x, "Simple AI is already at or beyond requested x tile coordinate after moving right for 0.1 seconds.")
