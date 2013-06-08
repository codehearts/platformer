import unittest
from game.layers import texture_tile_map_layer
from game.tiles import TextureTileMap
from ..util.layers import assert_layer_factory
from ..util import custom_tile_types
from ..util.tileset import get_testing_tileset

class TestTextureTileMapLayer(unittest.TestCase):

	def setUp(self):
		custom_tile_types.setUp()

		self.graphic = None
		self.layer = None

	def tearDown(self):
		custom_tile_types.tearDown()

	expected_classes = {
		'default': texture_tile_map_layer.TextureTileMapLayer,
		'fixed': texture_tile_map_layer.FixedTextureTileMapLayer,
		'static': texture_tile_map_layer.TextureTileMapLayer,
		'static-fixed': texture_tile_map_layer.FixedTextureTileMapLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of a texture tile map layer via the layer factory."""
		tile_map = [
			[0,3,2],
			[2,3,0],
		]
		self.graphic = TextureTileMap(tile_map, get_testing_tileset(2,2))

		assert_layer_factory(self, 'texture tile map')
