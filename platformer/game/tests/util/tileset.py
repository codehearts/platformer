from game.settings.general_settings import TILE_SIZE
from game.tiles.tileset import Tileset, TilesetImage, TilesetConfig
from image import dummy_image

def get_testing_tileset(rows, cols):
	image = TilesetImage(dummy_image(cols*TILE_SIZE, rows*TILE_SIZE))
	config = TilesetConfig(get_valid_config_data()['JSON'])

	return Tileset('test', image, config)

def get_valid_config_data():
	"""Returns a dict with valid tileset config test data.

	This config makes use of custom tile types, string values,
	integer values, and boolean values.

	Tile values 2, 3, 4, 5, 6, and 7 are basic tiles.
	Tile value 1 is a custom tile that faces right.
	Tile value 3 is a custom2 tile.
	Tile value 5 is positioned at 32, 128
	Tile value 7 is not collidable.

	Returns:
		A dict with two keys: "JSON", which contains the JSON encoded
		string for initializing a TilesetConfig object, and "expected",
		which is a Python dict of the expected results from parsing
		the JSON string.
	"""
	# Valid JSON config for testing
	JSON_config = '''{
		"1": {
			"type": "custom",
			"faces": "right"
		},
		"3": {
			"type": "custom2"
		},
		"5": {
			"x": 32,
			"y": 128
		},
		"7": {
			"is_collidable": false
		}
	}'''

	# Expected values for the parsed tileset config
	expected_config = {
		1: {
			'type': 'custom',
			'faces': 'right',
		},
		2: {},
		3: {
			'type': 'custom2',
		},
		4: {},
		5: {
			'x': 32,
			'y': 128,
		},
		6: {},
		7: {
			'is_collidable': False,
		},
		8: {},
	}

	return {
		'JSON': JSON_config,
		'expected': expected_config
	}
