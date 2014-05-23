import unittest
from ..load.tile_map import load_tile_map, arrange_tile_map
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

    def test_arrange_tile_map(self):
        """Tests the arrangement of a tile map from having its origin at the bottom left to the top right corner."""
        tile_map = [
            [0,1],
            [1,0],
        ]

        expected_tile_map = [
            [1,0],
            [0,1],
        ]

        self.assertEqual(arrange_tile_map(tile_map), expected_tile_map,
            "Failed to arrange 2x2 tile map.")

        tile_map = [
            [0,1,0],
            [1,0,1],
        ]

        expected_tile_map = [
            [1,0,1],
            [0,1,0],
        ]

        self.assertEqual(arrange_tile_map(tile_map), expected_tile_map,
            "Failed to arrange 3x2 tile map.")

        tile_map = [
            [0,1],
            [1,0],
            [3,4],
        ]

        expected_tile_map = [
            [3,4],
            [1,0],
            [0,1],
        ]

        self.assertEqual(arrange_tile_map(tile_map), expected_tile_map,
            "Failed to arrange 2x3 tile map.")
