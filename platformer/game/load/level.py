from pyglet.resource import file as open_resource_file
from game.bounded_box import BoundedBox
from game.graphics import create_graphics_object
from game.tiles import Tileset
from game import viewport
from json import load as json_load
from ..settings.general_settings import TILE_SIZE, RESOURCE_PATH, LEVEL_DIRECTORY, LEVEL_FORMAT, MAP_DIRECTORY, MAP_FORMAT, SCRIPT_DIRECTORY, SCRIPT_FORMAT
from game import layers
from imp import load_source
from sys import modules
"""Python 3
import importlib.machinery"""

# TODO Level loader tests
class Level(object):
    # TODO Documentation

    def __init__(self, level_data, key_handler):
        """Loads a level from disk.

        Args:
                level_data (dict): A dictionary of level parameters.
                key_handler (pyglet.window.key.KeyStateHandler): The key handler for the game.
        """
        self.title = level_data['title']

        camera_target = None

        # Load tilesets
        tilesets = {}
        for tileset in level_data['tilesets']:
            tilesets[tileset] = Tileset.load(tileset)

        # Check if the boundaries of the map were specified
        size_specified = 'size' in level_data
        if size_specified:
            rows = level_data['size'][1]
            cols = level_data['size'][0]
        else:
            rows = cols = 0

        self._load_scripts(level_data['scripts'])

        # Load layers
        level_layers = []
        self.layer_dict = {} # TODO Temporary method of accessing layers by title
        for layer_data in level_data['layers']:
            graphic_data = layer_data['graphic_data']

            # Apply data values to the level data
            if 'data_values' in layer_data:
                for data_property, data_value in layer_data['data_values'].iteritems():
                    self._apply_data_value(layer_data, data_property, data_value)

            # Drop in the tileset object if necessary
            if 'tileset' in graphic_data:
                graphic_data['tileset'] = tilesets[graphic_data['tileset']]

            # Drop in the key_handler object if necessary
            if 'key_handler' in graphic_data:
                graphic_data['key_handler'] = key_handler

            # Load the value map if necessary
            if 'value_map' in graphic_data:
                # TODO _load_map Should rearrange the stage array instead of making other classes do it
                graphic_data['value_map'] = self._load_map(graphic_data['value_map'])

                # If the boundaries of the map weren't specified, interpret them
                if not size_specified:
                    if len(graphic_data['value_map']) > cols:
                        cols = len(graphic_data['value_map'])
                    if len(graphic_data['value_map'][0]) > rows:
                        rows = len(graphic_data['value_map'][0])

            # TODO Remove the need for this hotfix
            # Get the tiles from the stage layer for the character
            if 'stage_layer' in graphic_data:
                graphic_data['stage'] = self.layer_dict[graphic_data['stage_layer']].graphic.tiles
                del graphic_data['stage_layer']

            layer_graphic = create_graphics_object(layer_data['graphic_type'], **graphic_data)

            # TODO Remove the need for this hotfix
            if layer_data['title'] == 'player':
                layer_graphic = layer_graphic.character

            if 'layer_data' in layer_data:
                layer = layers.create_from(layer_graphic, **layer_data['layer_data'])
            else:
                layer = layers.create_from(layer_graphic)

            if level_data['camera_target'] == layer_data['title']:
                camera_target = layer.graphic

            level_layers.append(layer)
            self.layer_dict[layer_data['title']] = layer

        stage_boundary = BoundedBox(0, 0, cols*TILE_SIZE, rows*TILE_SIZE)
        # TODO Don't hardcode window size, make it a global setting
        self.camera = viewport.Camera(0, 0, 800, 600, bounds=stage_boundary, target=camera_target)
        self.camera.focus() # TODO Should this be called on init?

        self.layer_manager = layers.LayerManager(self.camera, level_layers)

    def _load_map(self, map_name):
        """Loads the given level map from disk.

        Args:
            map_name (str): The name of the map to load.

        Returns:
            A 2d list of tile values.
        """
        # TODO Cache these files while initially loading the level, then clear the cache
        map_file = open_resource_file(MAP_DIRECTORY+'/'+map_name+'.'+MAP_FORMAT)
        map_data = json_load(map_file)
        map_file.close()

        return map_data

    def _apply_data_value(self, layer_data, data_property, data_value):
        layer_property = layer_data
        while data_property.rfind('.') > 0:
            layer_property = layer_property[data_property[ : data_property.find(".")]]
            data_property = data_property[data_property.rfind(".")+1 : ]

        module_name = data_value[ : data_value.rfind('.')]
        property_name = data_value[data_value.rfind('.')+1 : ]
        layer_property[data_property] = getattr(modules[module_name], property_name)

    def _load_scripts(self, scripts):
        """Dynamically loads the given scripts. The scripts are loaded from the scripts directory.

        Args:
            scripts (list): A list of the filenames of the scripts to load.
        """
        for script in scripts:
            load_source('scripts.'+script, RESOURCE_PATH+SCRIPT_DIRECTORY+'/'+script+'.'+SCRIPT_FORMAT)
            """Python 3
            loader = importlib.machinery.SourceFileLoader('scripts.'+script, RESOURCE_PATH+SCRIPT_DIRECTORY+'/'+script+'.'+SCRIPT_FORMAT)
            loader.load_module('scripts.'+script)"""

    @classmethod
    def load(cls, level_title, key_handler):
        # TODO The game.level.Level class in the doc should be updated once this class is finalized
        """Loads a level from a given level title.

        Args:
                level_title (str): The title of the level to load.
                key_handler (pyglet.window.key.KeyStateHandler): The key handler for the game.

        Returns:
                A :class:`game.level.Level` object.
        """
        level_file = open_resource_file(LEVEL_DIRECTORY+'/'+level_title+'.'+LEVEL_FORMAT)
        level_data = json_load(level_file)
        level_file.close()

        return cls(level_data, key_handler)
