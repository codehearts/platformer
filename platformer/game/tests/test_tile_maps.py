import unittest
from game.tiles.tile_map import TileMap
from game.tiles.texture_tile_map import TextureTileMap
from util.tileset import get_testing_tileset

class TestTileMap(unittest.TestCase):

	def setUp(self):
		self.tile_map_class = None
		self.tileset = get_testing_tileset(4, 4)



	def test_tile_map_layout(self):
		"""Tests TileMap to ensure that it lays out the map correctly."""
		# Test with the TileMap class
		self.tile_map_class = TileMap
		self.assert_tile_map_layout()

	def test_texture_tile_map_layout(self):
		"""Tests TextureTileMap to ensure that it lays out the map correctly."""
		# Test with the TileMap class
		self.tile_map_class = TextureTileMap
		self.assert_tile_map_layout()

	def assert_tile_map_layout(self):
		"""Asserts that the tile map class lays out the map correctly."""
		test_map = [
			[0,0],
			[0,0],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		# Map dimensions should be 2 by 2
		self.assertEqual(2, len(self.tile_map.tiles),
			"Tile map has incorrect number of rows.")
		self.assertEqual(2, len(self.tile_map.tiles[0]),
			"Tile map has incorrect number of columns.")

		# All tiles should be None
		for i in xrange(len(self.tile_map.tiles)):
			for j in xrange(len(self.tile_map.tiles[i])):
				self.assertIsNone(self.tile_map.tiles[i][j],
					"2x2 empty tile map is not actually empty.")


		# Test for bottom-left aligned anchor point
		# [0][1] in this list should map out to [2][1] in the tile array
		test_map = [
			[0,1,0],
			[0,0,0],
			[0,0,0],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		# 0 indexing on the y axis should now be inverted
		self.assertIsNotNone(self.tile_map.tiles[2][1], "Tile map does not have anchor point at bottom left.")


		# Test for bottom-left aligned anchor point by checking where various empty tiles end up
		test_map = [
			[ 1, 2, 1, 0],
			[ 2, 1, 3, 1],
			[ 7, 2, 0, 1],
			[ 1, 0, 6, 5],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		# Check if the empty tiles are where they should be
		self.assertIsNone(self.tile_map.tiles[0][1],
			"Tile map was created incorrectly.")
		self.assertIsNone(self.tile_map.tiles[1][2],
			"Tile map was created incorrectly.")
		self.assertIsNone(self.tile_map.tiles[3][3],
			"Tile map was created incorrectly.")

		# Check if the other tiles were created properly in the right place
		self.assertFalse(self.tile_map.tiles[1][0].is_collidable,
			"Tile map failed to correctly place non-collidable tile.")
		self.assertEqual(self.tile_map.tiles[3][0].type, 'custom',
			"Tile map failed to correctly place custom tile.")
		self.assertEqual(self.tile_map.tiles[0][2].type, 'basic',
			"Tile map failed to correctly place basic tile.")
		self.assertEqual(self.tile_map.tiles[0][3].x, 32,
			"Tile map failed to correctly initialize basic tile.")
		self.assertEqual(self.tile_map.tiles[0][3].y, 128,
			"Tile map failed to correctly initialize basic tile.")
		self.assertEqual(self.tile_map.tiles[2][2].type, 'custom2',
			"Tile map failed to correctly place custom2 tile.")



	def test_texture_tile_map_draw_region(self):
		"""Tests TextureTileMap region drawing to ensure that only the
		requested region is drawn."""
		# Test with the TileMap class
		self.tile_map_class = TextureTileMap

		test_map = [
			[ 1, 1, 1, 0],
			[ 1, 1, 1, 1],
			[ 1, 1, 0, 1],
			[ 1, 0, 1, 1],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		pass


# TODO Test TextureTileMap texture
# TODO If TileMap is not deprecated, test draw_region, set_batch, and set_group
