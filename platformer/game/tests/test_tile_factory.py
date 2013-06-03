import custom_tile_types, unittest
from game.settings.general_settings import TILE_SIZE
from game.tiles.tile import Tile
from game.tiles.tile_factory import create_tile
from util.image import dummy_image

class TestTileFactory(unittest.TestCase):
	"""Tests tile creation via the tile factory."""

	def setUp(self):
		# Disable any custom tile type callbacks which have already been set
		custom_tile_types.setUp()

		self.expected_x = None
		self.expected_y = None
		self.expected_is_collidable = None
		self.expected_tile_class = None
		self.expected_tile_type = None

		self.test_image = dummy_image(TILE_SIZE, TILE_SIZE)
		self.test_tile = None

	def tearDown(self):
		# Restore custom tile type callbacks
		custom_tile_types.tearDown()



	def test_basic_tile_factory(self):
		"""Tests the tile factory when no custom tile types are set."""

		self.expected_tile_class = Tile
		self.expected_tile_type = 'basic'
		self.expected_x = 0
		self.expected_y = 0
		self.expected_is_collidable = True

		# Test creating a typeless tile without arguments
		self.test_tile = create_tile(img=self.test_image)

		self.assert_tile('Given no type or arguments.')

		# Test creating a typeless tile with arguments
		self.expected_x = TILE_SIZE
		self.expected_y = TILE_SIZE * 2
		self.expected_is_collidable = False

		self.test_tile = create_tile(img=self.test_image, x=self.expected_x, y=self.expected_y, is_collidable=self.expected_is_collidable)

		self.assert_tile('Given no type, but arguments.')

		# Test creating a basic tile without arguments
		self.expected_x = 0
		self.expected_y = 0
		self.expected_is_collidable = True

		self.test_tile = create_tile(img=self.test_image, type='basic')

		self.assert_tile('Given type "basic" with no arguments.')

		# Test creating a typeless tile with arguments
		self.expected_x = TILE_SIZE * 3
		self.expected_y = TILE_SIZE
		self.expected_is_collidable = False

		self.test_tile = create_tile(img=self.test_image, type='basic', x=self.expected_x, y=self.expected_y, is_collidable=self.expected_is_collidable)

		self.assert_tile('Given type "basic" with arguments.')

		# Test creating a tile with a bogus type without arguments
		self.expected_x = 0
		self.expected_y = 0
		self.expected_is_collidable = True

		self.test_tile = create_tile(img=self.test_image, type='bogus')

		self.assert_tile('Given bogus type with no arguments.')

		# Test creating a tile of a nonexistent type with arguments
		self.expected_x = TILE_SIZE * 3
		self.expected_y = TILE_SIZE
		self.expected_is_collidable = False

		self.test_tile = create_tile(img=self.test_image, type='bogus', x=self.expected_x, y=self.expected_y, is_collidable=self.expected_is_collidable)

		self.assert_tile('Given bogus type with arguments.')



	def test_custom_tile_factory(self):
		"""Tests the tile factory when a single custom tile type is set.

		Basic tile creation is also tested by this method to ensure
		that it is still functional.
		"""

		# Register the "custom" tile type
		custom_tile_types.register_custom()

		# Test creating a custom tile facing right with only custom tile arguments
		self.expected_tile_class = custom_tile_types.RightFacingTile
		self.expected_tile_type = 'custom'
		self.expected_x = 0
		self.expected_y = 0
		self.expected_is_collidable = True

		self.test_tile = create_tile(img=self.test_image, type=self.expected_tile_type, faces='right')

		self.assert_tile('Given type "custom" with only custom tile arguments.')

		# Test creating a custom tile facing left with arguments
		self.expected_tile_class = custom_tile_types.LeftFacingTile
		self.expected_x = TILE_SIZE
		self.expected_y = TILE_SIZE * 2
		self.expected_is_collidable = False

		self.test_tile = create_tile(img=self.test_image, type=self.expected_tile_type, x=self.expected_x, y=self.expected_y, is_collidable=self.expected_is_collidable, faces='left')

		self.assert_tile('Given type "custom" with arguments.')

		# Test creating a custom tile without arguments
		self.expected_tile_class = custom_tile_types.UpFacingTile # Factory default
		self.expected_x = 0
		self.expected_y = 0
		self.expected_is_collidable = True

		self.test_tile = create_tile(img=self.test_image, type=self.expected_tile_type)

		self.assert_tile('Given type "custom" with no arguments.')

		# Ensure that basic tile creation still functions
		self.test_basic_tile_factory()



	def test_custom2_tile_factory(self):
		"""Tests the tile factory when multiple custom tile types are set.

		Basic tile creation is also tested by this method to ensure
		that it is still functional.
		"""

		# Register all custom tile types
		custom_tile_types.register_all()

		# Test creating a custom2 tile with no arguments
		self.expected_tile_class = custom_tile_types.Custom2Tile
		self.expected_tile_type = 'custom2'
		self.expected_x = 0
		self.expected_y = 0
		self.expected_is_collidable = True

		self.test_tile = create_tile(img=self.test_image, type=self.expected_tile_type)

		self.assert_tile('Given type "custom2" with no arguments.')

		# Test creating a custom2 tile with arguments
		self.expected_x = TILE_SIZE
		self.expected_y = TILE_SIZE * 2
		self.expected_is_collidable = False

		self.test_tile = create_tile(img=self.test_image, type=self.expected_tile_type, x=self.expected_x, y=self.expected_y, is_collidable=self.expected_is_collidable)

		self.assert_tile('Given type "custom2" with arguments.')

		# Ensure that creation of the other custom tile type still functions
		# This method also tests that basic tile creation still works
		self.test_custom_tile_factory()



	# Helper methods



	def assert_tile(self, condition=''):
		"""Asserts that the tile object is configured correctly."""
		if condition:
			condition = ' Condition: '+condition

		self.assertTrue(type(self.test_tile) is self.expected_tile_class, "Tile factory failed to create correct tile object." + condition)
		self.assertEqual(self.test_tile.type, self.expected_tile_type, "Tile factory failed to create tile with correct type attribute." + condition)
		self.assertEqual(self.test_tile.x, self.expected_x, "Tile factory failed to set x coordinate of created tile." + condition)
		self.assertEqual(self.test_tile.y, self.expected_y, "Tile factory failed to set y coordinate of created tile." + condition)
		self.assertEqual(self.test_tile.is_collidable, self.expected_is_collidable, "Tile factory failed to set is_collidable attribute of created tile." + condition)
