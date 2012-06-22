import pyglet, unittest
from game import load, bestiary, util
from game.settings import demo_settings, player_settings

class TestLoaders(unittest.TestCase):
    
    """
    Tests the loader for the stage
    """
    def test_stage_loader(self):
        tile_data = demo_settings.TILE_DATA
        test_map = [
            [0,0],
            [0,0]
        ]
        
        tiles = load.Stage(tile_data, test_map).get_tiles()
        
        # Stage dimensions should be 2 by 2
        self.assertEqual(2, len(tiles))
        self.assertEqual(2, len(tiles[0]))
        
        # All tiles should be None
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                self.assertIsNone(tiles[i][j])
        
        
        
        # Test for bottom-left aligned anchor point
        # [0][1] in this list should map out to [2][1] in the tile array
        test_map = [
            [0,1,0],
            [0,0,0],
            [0,0,0]
        ]
        
        tiles = load.Stage(tile_data, test_map).get_tiles()
        
        # 0 indexing on the y axis should now be inverted
        self.assertTrue(not (tiles[2][1] == None))
        
        
        
        # Test for bottom-left aligned anchor point by checking where various empty tiles end up
        test_map = [
            [ 1, 1, 1,00],
            [ 1, 1, 1, 1],
            [ 1, 1,00, 1],
            [ 1,00, 1, 1]
        ]
        
        tiles = load.Stage(tile_data, test_map).get_tiles()
        
        # Check if the empty tiles are where they should be
        self.assertIsNone(tiles[0][1])
        self.assertIsNone(tiles[1][2])
        self.assertIsNone(tiles[3][3])
    
    
    
    """
    Tests the loader for the playable character
    """
    def test_player_loader(self):
        # Set up our tests
        empty_map = [
            [0,0],
            [0,0]
        ]
        tiles = load.Stage(demo_settings.TILE_DATA, empty_map).get_tiles()
        
        test_player_data = [
            # Test 1
            {
                'initial_values': {
                    'x': 1,
                    'y': 1
                },
                'expected_results': {
                    'get_acceleration': (0, util.get_gravitational_acceleration(player_settings.MASS)),
                    'get_coordinates': util.tile_to_coordinate(1, 1)
                }
            },
            
            # Test 2
            {
                'initial_values': {
                    'x': 7.23,
                    'y': 2.39
                },
                'expected_results': {
                    'get_coordinates': util.tile_to_coordinate(7.21875, 2.375) # Characters can only be placed full-pixel intervals
                }
            }
        ]
        
        # Run each test
        for test in test_player_data:
            # Load the player
            player = load.Player(test['initial_values'], tiles).character
            expected_results = test['expected_results']
            
            # Call each method on the player and check the results
            for method, value in expected_results.iteritems():
                self.assertEqual(expected_results[method], getattr(player, method)())
    
    
    """
    Tests the loader for all non-playable characters
    """
    def test_characters_loader(self):
        # Set up our tests
        empty_map = [
            [0,0],
            [0,0]
        ]
        tiles = load.Stage(demo_settings.TILE_DATA, empty_map).get_tiles()
        
        test_character_data = [
            # Test 1
            # Single character, no gravity
            {
                'initial_values': {
                    'test_object_1': {
                        'x': 1,
                        'y': 1
                    }
                },
                'expected_results': [
                    {
                        'get_acceleration': (0, util.get_gravitational_acceleration(bestiary.look_up['test_object_1']['mass'])),
                        'get_coordinates': util.tile_to_coordinate(1, 1)
                    }
                ]
            },
            
            # Test 2
            # Two characters, no gravity
            {
                'initial_values': {
                    'test_object_2': {
                        'x': 1.5,
                        'y': 3
                    },
                    'test_object_3': {
                        'x': 9.25,
                        'y': 1.99
                    }
                },
                'expected_results': [
                    {
                        'get_acceleration': (0, util.get_gravitational_acceleration(bestiary.look_up['test_object_2']['mass'])),
                        'get_coordinates': util.tile_to_coordinate(1.5, 3)
                    },
                    {
                        'get_acceleration': (0, util.get_gravitational_acceleration(bestiary.look_up['test_object_3']['mass'])),
                        'get_coordinates': (296, 63)  # Characters can only be placed full-pixel intervals
                    }
                ]
            }
        ]
        
        # Run each test
        for test in test_character_data:
            # Load the characters
            characters = load.Characters(test['initial_values'], tiles).get_characters()
            
            # Check each character against the expected results
            for i in range(len(characters)):
                character = characters[i]
                expected_results = test['expected_results'][i]
                
                # Call each method on the character and check the results
                for method, value in expected_results.iteritems():
                    self.assertEqual(expected_results[method], getattr(character, method)())