from json import load as json_load
from pyglet.resource import file as open_resource_file
from ..settings.general_settings import MAP_DIRECTORY, MAP_FORMAT

def load_tile_map(map_name):
    """Loads the given level map from disk.

    Args:
        map_name (str): The name of the map to load.

    Returns:
        A 2d list of tile values.
    """
    # TODO Cache these file contents while initially loading the level, then clear the cache
    map_file = open_resource_file(MAP_DIRECTORY+'/'+map_name+'.'+MAP_FORMAT)
    map_data = json_load(map_file)
    map_file.close()

    return arrange_tile_map(map_data)

def arrange_tile_map(tile_map):
    rows = len(tile_map)
    cols = len(tile_map[0])

    # Flip the map vertically because we want index [0][0] to represent the bottom left corner of the map
    for y in xrange(rows / 2):
        for x in xrange(cols):
            adjusted_y = rows - y - 1; # Verically flipped y index
            temp_value = tile_map[adjusted_y][x]
            tile_map[adjusted_y][x] = tile_map[y][x]
            tile_map[y][x] = temp_value

    return tile_map
