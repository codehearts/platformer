from pyglet.resource import file as open_resource_file
from game.bounded_box import BoundedBox
from game.graphics import create_graphics_object
from game import viewport
from json import load as json_load
from ..settings.general_settings import TILE_SIZE, RESOURCE_PATH, LEVEL_DIRECTORY, LEVEL_FORMAT, SCRIPT_DIRECTORY, SCRIPT_FORMAT
from game import layers
from imp import load_source, new_module
from sys import modules
from tile_map import load_tile_map
from installed_level_config_translators import install_level_config_translator, translate_data_value
import game.scripts
"""Python 3
import importlib.machinery"""

# TODO Level loader tests
class Level(object):
    # TODO Documentation

    def __init__(self, level_data):
        """Loads a level from disk.

        Args:
            level_data (dict): A dictionary of level parameters.
        """
        # Add support for translating config strings to property values
        install_level_config_translator('property', self._get_property_from_string)

        # Scripts must be loaded first because they provide dynamic values which may be used
        self._load_scripts(level_data['scripts'])

        self.title = translate_data_value(level_data['title'])

        camera_target = None

        # Check if the boundaries of the map were specified
        size_specified = 'size' in level_data
        if size_specified:
            rows = translate_data_value(level_data['size'][1])
            cols = translate_data_value(level_data['size'][0])

        # Load layers
        level_layers = []
        self.layer_dict = {} # TODO Temporary method of accessing layers by title
        for layer_data in level_data['layers']:
            # Translate all graphics data values
            layer_data['graphic_data'] = dict(map(lambda (k,v) : (k, translate_data_value(v)), layer_data['graphic_data'].iteritems()))
            graphic_data = layer_data['graphic_data']

            # Translate all layer data values
            if 'layer_data' in layer_data:
                layer_data['layer_data'] = dict(map(lambda (k,v) : (k, translate_data_value(v)), layer_data['layer_data'].iteritems()))

            # TODO Remove the need for this hotfix
            # Get the tiles from the stage layer for the character
            if 'stage_layer' in graphic_data:
                # TODO Should just pass a reference to the stage or something here instead of having this class be aware of what to do
                graphic_data['stage'] = self.layer_dict[graphic_data['stage_layer']].graphic.tiles
                del graphic_data['stage_layer']

            layer_graphic = create_graphics_object(translate_data_value(layer_data['graphic_type']), **graphic_data)

            # TODO Remove the need for this hotfix
            if translate_data_value(layer_data['title']) == 'player':
                layer_graphic = layer_graphic.character

            if 'layer_data' in layer_data:
                layer = layers.create_from(layer_graphic, **layer_data['layer_data'])
            else:
                layer = layers.create_from(layer_graphic)

            if translate_data_value(level_data['camera_target']) == layer_data['title']:
                camera_target = layer.graphic

            level_layers.append(layer)
            self.layer_dict[translate_data_value(layer_data['title'])] = layer

        # TODO If the size isn't specified, an unbounded camera should be used in place of this hotfix
        if not size_specified:
            rows = cols = 1000

        stage_boundary = BoundedBox(0, 0, cols*TILE_SIZE, rows*TILE_SIZE)
        # TODO Don't hardcode window size, make it a global setting
        self.camera = viewport.Camera(0, 0, 800, 600, bounds=stage_boundary, target=camera_target)
        self.camera.focus() # TODO Should this be called on init?

        self.layer_manager = layers.LayerManager(self.camera, level_layers)

    def _get_property_from_string(self, property_value):
        split = property_value.rfind('.')
        module_name = property_value[ : split]
        property_name = property_value[split +1 : ]
        return getattr(modules[module_name], property_name)

    def _load_scripts(self, scripts):
        """Dynamically loads the given scripts. The scripts are loaded from the scripts directory.

        Args:
            scripts (list): A list of the filenames of the scripts to load.
        """
        for script in scripts:
            load_source('game.scripts.custom.'+script, RESOURCE_PATH+SCRIPT_DIRECTORY+'/'+script+'.'+SCRIPT_FORMAT)
            """Python 3
            loader = importlib.machinery.SourceFileLoader('games.scripts.custom.'+script, RESOURCE_PATH+SCRIPT_DIRECTORY+'/'+script+'.'+SCRIPT_FORMAT)
            loader.load_module('game.scripts.custom.'+script)"""

    @classmethod
    def load(cls, level_title):
        # TODO The game.level.Level class in the doc should be updated once this class is finalized
        """Loads a level from a given level title.

        Args:
            level_title (str): The title of the level to load.

        Returns:
            A :class:`game.level.Level` object.
        """
        level_file = open_resource_file(LEVEL_DIRECTORY+'/'+level_title+'.'+LEVEL_FORMAT)
        level_data = json_load(level_file)
        level_file.close()

        return cls(level_data)
