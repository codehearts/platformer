from pyglet.resource import get_script_home

FPS = 120.0
FRAME_LENGTH = 1 / FPS
TILE_SIZE = 32
TILE_SIZE_FLOAT = float(TILE_SIZE)
GRAVITY = 9.8

RESOURCE_PATH = get_script_home() + '/resources/'
TILESET_DIRECTORY = 'tilesets'
LEVEL_DIRECTORY = 'levels'
LEVEL_FORMAT = 'json'
MAP_DIRECTORY = 'maps'
MAP_FORMAT = 'json'
SCRIPT_DIRECTORY = 'scripts'
SCRIPT_FORMAT = 'py'
