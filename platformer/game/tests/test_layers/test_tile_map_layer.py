import unittest
from game.layers import tile_map_layer
from game.tiles import TileMap
from ..util import custom_tile_types
from ..util.layers import assert_layer_factory
from ..util.tileset import get_testing_tileset

class TestTileMapLayer(unittest.TestCase):

	def setUp(self):
		custom_tile_types.setUp()

		self.graphic = None
		self.layer = None

	def tearDown(self):
		custom_tile_types.tearDown()

	expected_classes = {
		'default': tile_map_layer.TileMapLayer,
		'fixed': tile_map_layer.TileMapLayer,
		'static': tile_map_layer.TileMapLayer,
		'static-fixed': tile_map_layer.TileMapLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of a tile map layer via the layer factory."""
		tile_map = [
			[0,1,2],
			[2,1,0],
		]
		self.graphic = TileMap(tile_map, get_testing_tileset(2,2))

		assert_layer_factory(self, 'tile map')
