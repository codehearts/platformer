import unittest
from game.settings.general_settings import TILE_SIZE
from game.tiles.tileset import TilesetImage
from pyglet.image import TextureGrid, ImageGrid
from ..util.image import dummy_image

class TestTilesetImage(unittest.TestCase):
	"""Tests management of a tileset image."""

	def setUp(self):
		self.expected_tile_width = None
		self.expected_tile_height = None
		self.expected_rows = None
		self.expected_cols = None

		self.test_image = None
		self.tileset_image = None



	def test_unbounded_tileset_image(self):
		"""Tests creating a TilesetImage without specifying the rows and columns in the image."""
		# Create an 8x6 tileset image placeholder
		self.expected_tile_width = 8
		self.expected_tile_height = 6
		self.expected_rows = self.expected_tile_height
		self.expected_cols = self.expected_tile_width

		self.test_image = dummy_image(self.expected_width(), self.expected_height())
		self.test_image_grid = TextureGrid(ImageGrid(self.test_image, self.expected_rows, self.expected_cols))

		# Test creating a TilesetImage without specifying dimensions
		self.tileset_image = TilesetImage(self.test_image)

		self.assert_tileset_image('Rows and columns not specified.')

	def test_bounded_tileset_image(self):
		"""Tests creating a TilesetImage with specific rows and columns in the image."""
		# Create an 8x6 tileset image placeholder
		self.expected_tile_width = 8
		self.expected_tile_height = 6
		self.expected_rows = 5
		self.expected_cols = 4

		self.test_image = dummy_image(self.expected_width(), self.expected_height())
		self.test_image_grid = TextureGrid(ImageGrid(self.test_image, self.expected_rows, self.expected_cols))

		# Test creating a TilesetImage with specific dimensions
		self.tileset_image = TilesetImage(self.test_image, rows=self.expected_rows, cols=self.expected_cols)

		self.assert_tileset_image('Rows and columns not specified.')



	# Helper methods

	def assert_tileset_image(self, condition=''):
		"""Asserts that the tileset image coordinates are correct."""
		if condition:
			condition = ' Condition: '+condition

		# Check dimensions
		self.assertEqual(self.tileset_image.rows, self.expected_rows, "Tileset image has incorrect number of rows." + condition)
		self.assertEqual(self.tileset_image.cols, self.expected_cols, "Tileset image has incorrect number of columns." + condition)

		# Check retrieval of tile images

		# Test getting tile image at top left corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.top_left_tile_value()).tex_coords,
			self.test_image_grid[self.expected_rows-1, 0].tex_coords,
			"Tileset image has incorrect tile image for top left tile value." + condition
		)

		# Test getting tile image at bottom right corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.bottom_right_tile_value()).tex_coords,
			self.test_image_grid[0, self.expected_cols-1].tex_coords,
			"Tileset image has incorrect tile image for bottom right tile value." + condition
		)

		# Test getting tile image at top right corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.top_right_tile_value()).tex_coords,
			self.test_image_grid[self.expected_rows-1, self.expected_cols-1].tex_coords,
			"Tileset image has incorrect tile image for top right tile value." + condition
		)

		# Test getting tile image at bottom left corner
		self.assertEqual(
			self.tileset_image.get_tile_image(self.bottom_left_tile_value()).tex_coords,
			self.test_image_grid[0, 0].tex_coords,
			"Tileset image has incorrect tile image for bottom left tile value." + condition
		)

		# Check caching of tile image data

		first_call = self.tileset_image.get_tile_image_data(self.top_left_tile_value())
		second_call = self.tileset_image.get_tile_image_data(self.top_left_tile_value())

		self.assertIs(first_call, second_call, "Tileset image failed to cache image data for first tile value." + condition)

		# Check for a different tile value
		first_call = self.tileset_image.get_tile_image_data(self.bottom_right_tile_value())
		second_call = self.tileset_image.get_tile_image_data(self.bottom_right_tile_value())

		self.assertIs(first_call, second_call, "Tileset image failed to cache image data for second tile value." + condition)



	def expected_width(self):
		"""Returns the pixel width of the image for the current test dimensions."""
		return self.expected_tile_width * TILE_SIZE

	def expected_height(self):
		"""Returns the pixel height of the image for the current test dimensions."""
		return self.expected_tile_height * TILE_SIZE

	def top_right_tile_value(self):
		"""Returns the tile value of the top right tile image for the current test dimensions."""
		return self.expected_cols

	def top_left_tile_value(self):
		"""Returns the tile value of the top left tile image for the current test dimensions."""
		return 1

	def bottom_right_tile_value(self):
		"""Returns the tile value of the bottom right tile image for the current test dimensions."""
		return self.expected_rows * self.expected_cols

	def bottom_left_tile_value(self):
		"""Returns the tile value of the bottom left tile image for the current test dimensions."""
		return self.expected_cols * (self.expected_rows - 1) + 1
