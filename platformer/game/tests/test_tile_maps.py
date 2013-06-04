import unittest
from game.tiles.tile_map import TileMap
from game.tiles.texture_tile_map import TextureTileMap
from game.settings.general_settings import TILE_SIZE
from pyglet.graphics import Batch, Group
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



	def test_tile_map_visible_region(self):
		"""Tests setting the visible region of a TileMap to ensure that
		only the requested region is visible."""
		# Test with the TileMap class
		self.tile_map_class = TileMap

		test_map = [
			[ 1, 1, 1, 0],
			[ 1, 1, 1, 1],
			[ 1, 1, 0, 1],
			[ 1, 0, 1, 1],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		# Test with multiples of tile sizes
		self.tile_map.set_visible_region(
			x =		    TILE_SIZE,	y =			    TILE_SIZE,
			width =	2 * TILE_SIZE,	height =	3 * TILE_SIZE
		)

		self.invisible_coordinates = [
			(0,3),					(3,3),
			(0,2),					(3,2),
			(0,1),					(3,1),
			(0,0),	(1,0),	(2,0),	(3,0),
		]

		self.visible_coordinates = [
			(1,3),	(2,3),
			(1,2),	(2,2),
			(1,1),	(2,1),
		]

		self.assert_tile_map_visible_region()

		# Test changing the region slightly
		self.tile_map.set_visible_region(
			x =		0 * TILE_SIZE,	y =			    TILE_SIZE,
			width =	2 * TILE_SIZE,	height =	2 * TILE_SIZE
		)

		self.invisible_coordinates = [
			(0,3),	(1,3),	(2,3),	(3,3),
							(2,2),	(3,2),
							(2,1),	(3,1),
			(0,0),	(1,0),	(2,0),	(3,0),
		]

		self.visible_coordinates = [
			(0,2),	(1,2),
			(0,1),	(1,1),
		]

		self.assert_tile_map_visible_region()

		# Test setting the region with floats
		self.tile_map.set_visible_region(
			x =		1.5 * TILE_SIZE,	y =			2.1  * TILE_SIZE,
			width =	0.5 * TILE_SIZE,	height =	2.71 * TILE_SIZE
		)

		self.invisible_coordinates = [
			(0,3),			(2,3),	(3,3),
			(0,2),			(2,2),	(3,2),
			(0,1),	(1,1),	(2,1),	(3,1),
			(0,0),	(1,0),	(2,0),	(3,0),
		]

		self.visible_coordinates = [
			(1,3),
			(1,2),
		]

		self.assert_tile_map_visible_region()

	def assert_tile_map_visible_region(self):
		"""Asserts that the tile map's visible region is correct."""
		# Ensure that tiles outside the region are invisible
		for coords in self.invisible_coordinates:
			tile = self.tile_map.tiles[coords[1]][coords[0]]
			if tile:
				self.assertFalse(tile.visible,
				"Failed to set tile outside of region as invisible.")

		# Ensure that tiles within the region are visible
		for coords in self.visible_coordinates:
			tile = self.tile_map.tiles[coords[1]][coords[0]]
			if tile:
				self.assertTrue(tile.visible,
				"Failed to set tile inside of region as visible.")



	def test_texture_tile_map_draw_region(self):
		"""Tests TextureTileMap region drawing to ensure that only the
		requested region is drawn."""
		# Test with the TextureTileMap class
		self.tile_map_class = TextureTileMap

		test_map = [
			[ 1, 1, 1, 0],
			[ 1, 1, 1, 1],
			[ 1, 1, 0, 1],
			[ 1, 0, 1, 1],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		# TODO Implement this. TextureTileMap should have a get_region method to make this test easier
		pass



	def test_tile_map_graphics_attributes(self):
		"""Tests setting the batch and group for tiles in a TileMap."""
		# Test with the TileMap class
		self.tile_map_class = TileMap

		test_map = [
			[ 1, 1, 1, 0],
			[ 1, 1, 0, 1],
			[ 1, 1, 0, 1],
			[ 1, 0, 1, 1],
		]

		# Create a batch and group for testing
		self.test_batch = Batch()
		self.test_group = Group()

		# Create a tile map with the batch and group
		self.tile_map = self.tile_map_class(
			test_map, self.tileset,
			batch=self.test_batch, group=self.test_group
		)

		# Assert that everything was set properly
		self.assert_tile_map_graphics_attributes()

		# Create a new batch and group and test setting them
		self.test_batch = Batch()
		self.test_group = Group()

		self.assertIsNot(self.test_batch, self.tile_map.tiles[0][0].batch,
			"New test batch is same as old test batch.")
		self.assertIsNot(self.test_group, self.tile_map.tiles[0][0].group,
			"New test group is same as old test group.")

		# Set the new batch and group
		self.tile_map.batch = self.test_batch
		self.tile_map.group = self.test_group

		# Assert that everything was updated
		self.assert_tile_map_graphics_attributes()

	def assert_tile_map_graphics_attributes(self):
		"""Asserts that the current test map's graphics attributes are correct."""
		for y in xrange(self.tile_map.rows):
			for x in xrange(self.tile_map.cols):
				tile = self.tile_map.tiles[y][x]
				if tile:
					self.assertIs(
						self.test_batch, tile.batch,
						"Tile map did not add tile to the correct graphics batch."
					)
					self.assertIs(
						self.test_group, tile.group,
						"Tile map did not add tile to the correct graphics group."
					)



# TODO Test TextureTileMap texture
# TODO If TileMap is not deprecated, test draw_region, set_batch, and set_group
