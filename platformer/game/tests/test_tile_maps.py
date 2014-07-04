import unittest
from game.tiles.tile_map import TileMap
from game.tiles.tileset import TilesetImage, Tileset
from game.tiles.texture_tile_map import TextureTileMap
from game.settings.general_settings import TILE_SIZE
from pyglet.graphics import Batch, Group
from pyglet.image import ImageGrid, TextureGrid
from util.image import dummy_image
from util.tileset import get_testing_tileset_config, get_testing_tileset

class TestTileMap(unittest.TestCase):

	def setUp(self):
		self.colors = [
			(255,  0,  0,255),
			(  0,255,  0,255),
			(  0,  0,255,255),
			(255,255,  0,255),
			(255,  0,255,255),
			(  0,255,255,255),
			(255,255,255,255),
			(  0,  0,  0,255),
		]

		self.tile_map_class = None
		self.tile_map = None
		self.tileset = get_testing_tileset(4, 4)



	def test_tile_map_layout(self):
		"""Tests TileMap to ensure that it lays out the map correctly."""
		# Test with the TileMap class
		self.tile_map_class = TileMap
		self.assert_tile_map_layout()

	def test_texture_tile_map_layout(self):
		"""Tests TextureTileMap to ensure that it lays out the map correctly."""
		# Test with the TextureTileMap class
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
		self.assertEqual(2, self.tile_map.rows,
			"Tile map has incorrect number of rows.")
		self.assertEqual(2, len(self.tile_map.tiles[0]),
			"Tile map has incorrect number of columns.")
		self.assertEqual(2, self.tile_map.cols,
			"Tile map has incorrect number of columns.")

		# All tiles should be None
		for i in xrange(len(self.tile_map.tiles)):
			for j in xrange(len(self.tile_map.tiles[i])):
				self.assertIsNone(self.tile_map.tiles[i][j],
					"2x2 empty tile map is not actually empty.")

		# Test for bottom-left aligned anchor point by checking where various empty tiles end up
		test_map = [
			[ 1, 2, 1, 0],
			[ 2, 1, 3, 1],
			[ 7, 2, 0, 1],
			[ 1, 0, 6, 5],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		self.assertEqual(4, self.tile_map.rows,
			"Tile map has incorrect number of rows.")
		self.assertEqual(4, self.tile_map.cols,
			"Tile map has incorrect number of columns.")

		# Check if the empty tiles are where they should be
		self.assertIsNone(self.tile_map.tiles[3][1],
			"Tile map was created incorrectly.")
		self.assertIsNone(self.tile_map.tiles[2][2],
			"Tile map was created incorrectly.")
		self.assertIsNone(self.tile_map.tiles[0][3],
			"Tile map was created incorrectly.")

		# Check if the other tiles were created properly in the right place
		self.assertFalse(self.tile_map.tiles[2][0].is_collidable,
			"Tile map failed to correctly place non-collidable tile.")
		self.assertEqual(self.tile_map.tiles[0][0].type, 'custom',
			"Tile map failed to correctly place custom tile.")
		self.assertEqual(self.tile_map.tiles[3][2].type, 'basic',
			"Tile map failed to correctly place basic tile.")
		self.assertEqual(self.tile_map.tiles[3][3].x, 32,
			"Tile map failed to correctly initialize basic tile.")
		self.assertEqual(self.tile_map.tiles[3][3].y, 128,
			"Tile map failed to correctly initialize basic tile.")
		self.assertEqual(self.tile_map.tiles[1][2].type, 'custom2',
			"Tile map failed to correctly place custom2 tile.")



	def test_texture_tile_map_texture(self):
		"""Tests TextureTileMap to ensure that its tile map texture is drawn correctly.

		This is done by creating a tileset image with different colors for
		each tile, and then creating a texture tile map with it. The tile
		map's texture then has its raw image data compared to each tile
		image's data to ensure that each tile region of the map has the
		correct color for that tile.
		"""
		# Test with the TextureTileMap class
		self.tile_map_class = TextureTileMap

		# Define differently colored images for each tile
		tile_images = []
		for color in self.colors:
			tile_images.append(dummy_image(TILE_SIZE, TILE_SIZE, color=color))

		# Create a patchworked image of different tile images
		tile_image = dummy_image(len(tile_images) * TILE_SIZE, TILE_SIZE)
		for i in range(len(tile_images)):
			tile_image.texture.blit_into(
				tile_images[i].get_image_data(),
				i * tile_images[i].width,
				tile_image.height - tile_images[i].height,
				0
			)

		# Create a test tileset with the patchworked tile sprite image
		tileset = Tileset('test', TilesetImage(tile_image.texture), get_testing_tileset_config())

		# Create a tile map
		test_map = [
			[ 1, 2, 7, 0],
			[ 4, 3, 5, 1],
			[ 5, 1, 0, 2],
			[ 6, 0, 1, 6],
		]

		self.tile_map = self.tile_map_class(test_map, tileset)

		# Raw image data formatting parameters
		data_format = 'RGBA'
		pitch = tile_images[0].width * len(data_format)

		# Create a texture grid of the map for easy tile region access
		tile_map_grid = TextureGrid(ImageGrid(
			self.tile_map.texture, len(test_map), len(test_map[0])
		))

		# Expected tile images and the coordinates where they should be
		expected_images = {
			1: [(0,0), (2,1), (3,2), (1,3)],
			2: [(0,1), (2,3)],
			3: [(1,1)],
			4: [(1,0)],
			5: [(2,0), (1,2)],
			6: [(3,0), (3,3)],
		}

		# Assert that each region of the texture has the correct tile image
		for tile_value, coords in expected_images.iteritems():
			# Get the tile image as raw image data
			expected_image_data = tileset.image.get_tile_image_data(tile_value).get_data(data_format, pitch)

			# Check each coordinate where it should be
			for coord in coords:
				self.assertEqual(
					tile_map_grid[coord].get_image_data().get_data(data_format, pitch),
					expected_image_data,
					"Texture tile map failed to draw tile onto texture correctly."
				)

			# Ensure that these tests are actually working by testing cases
			# which we know must be false
			if tile_value != 1:
				self.assertNotEqual(
					tile_map_grid[0,0].get_image_data().get_data(data_format, pitch),
					expected_image_data,
					"Texture tile map claims to have drawn a tile image where it claimed to have already drawn another tile image."
				)



	def test_tile_map_visible_region(self):
		"""Tests setting the visible region of a TileMap to ensure that only the requested region is visible."""
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



	def test_texture_tile_map_texture_region(self):
		"""Tests TextureTileMap texture regions to ensure that an appropriately sized region is returned.

		This is important for assuring efficient drawing of
		only the visible region of the texture.
		"""
		# Test with the TextureTileMap class
		self.tile_map_class = TextureTileMap

		test_map = [
			[ 1, 1, 1, 0],
			[ 1, 1, 1, 1],
			[ 1, 1, 0, 1],
			[ 1, 0, 1, 1],
		]

		self.tile_map = self.tile_map_class(test_map, self.tileset)

		# get_region arguments and the arguments for the expected returned region
		region_arguments = [
			[0, 0, TILE_SIZE, TILE_SIZE], # 1
			[-10, -10, TILE_SIZE, TILE_SIZE], # 2
			[0, 0, self.tile_map.cols*TILE_SIZE*2, self.tile_map.rows*TILE_SIZE*2], # 3
			[-10, -10, self.tile_map.cols*TILE_SIZE*2, self.tile_map.rows*TILE_SIZE*2], # 4
			[16, 16, TILE_SIZE*2, TILE_SIZE*2], # 5
			[16, 16, self.tile_map.cols*TILE_SIZE*2, self.tile_map.rows*TILE_SIZE*2], # 6
		]
		expected_regions = [
			[0, 0, TILE_SIZE, TILE_SIZE], # 1
			[0, 0, TILE_SIZE-10, TILE_SIZE-10], # 2
			[0, 0, self.tile_map.cols*TILE_SIZE, self.tile_map.rows*TILE_SIZE], # 3
			[0, 0, self.tile_map.cols*TILE_SIZE, self.tile_map.rows*TILE_SIZE], # 4
			[16, 16, 2*TILE_SIZE, 2*TILE_SIZE], # 5
			[16, 16, self.tile_map.cols*TILE_SIZE-16, self.tile_map.rows*TILE_SIZE-16], # 6
		]

		# Assert that the expected region is always returned
		for i in xrange(len(region_arguments)):
			# Returned texture region
			actual = self.tile_map.get_region(*region_arguments[i])

			self.assertEqual(actual.x, expected_regions[i][0],
				"Texture tile map did not create a region at the correct x coordinate.")
			self.assertEqual(actual.y, expected_regions[i][1],
				"Texture tile map did not create a region at the correct y coordinate.")
			self.assertEqual(actual.width, expected_regions[i][2],
				"Texture tile map did not create an appropriately wide region.")
			self.assertEqual(actual.height, expected_regions[i][3],
				"Texture tile map did not create an appropriately tall region.")



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
