import unittest
from ..load.tile_map import load_tile_map, arrange_tile_map

class TestLoadTileMap(unittest.TestCase):

        def test_load_tile_map(self):
            # TODO Write tests for loading tile map from JSON file
            pass

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
