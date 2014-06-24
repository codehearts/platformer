import unittest
from ..load.tile_map import load_tile_map
from util import resource

class TestLoadTileMap(unittest.TestCase):
    """Tests loading a tilemap from a config file."""

    @classmethod
    def setUpClass(cls):
        resource.setUp()

    @classmethod
    def tearDownClass(cls):
        resource.tearDown()



    def test_load_tile_map(self):
        tile_map = load_tile_map('test1')

        expected_tile_map = [
            [1,0],
            [0,1],
        ]

        self.assertEqual(tile_map, expected_tile_map,
            "Failed to properly 2x2 tile map.")

        tile_map = load_tile_map('test2')

        expected_tile_map = [
            [1,0,1],
            [0,1,0],
        ]

        self.assertEqual(tile_map, expected_tile_map,
            "Failed to properly load 3x2 tile map.")

        tile_map = load_tile_map('test3')

        expected_tile_map = [
            [3,4],
            [1,0],
            [0,1],
        ]

        self.assertEqual(tile_map, expected_tile_map,
            "Failed to properly load 2x3 tile map.")
