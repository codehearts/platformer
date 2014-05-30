from pyglet.resource import file as open_resource_file
from game.bounded_box import BoundedBox
from game.graphics import create_graphics_object
from game.tiles import Tileset
from game import viewport
from json import load as json_load
from ..settings.general_settings import TILE_SIZE, RESOURCE_PATH, LEVEL_DIRECTORY, LEVEL_FORMAT, SCRIPT_DIRECTORY, SCRIPT_FORMAT
from game import layers
from imp import load_source, new_module
from sys import modules
from tile_map import load_tile_map
import game.scripts
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
        # Dictionary of tags and translation functions to apply to config data values
        self._installed_translators = {}
        self._data_value_tag_prefix = ''
        self._data_value_tag_suffix = '::'

        # Add support for translating config strings to property values
        self.add_config_data_translator('property', self._get_property_from_string)

        # Scripts must be loaded first because they provide dynamic values which may be used
        self._load_scripts(level_data['scripts'])

        self.title = self._translate_data_value(level_data['title'])

        camera_target = None

        # Check if the boundaries of the map were specified
        size_specified = 'size' in level_data
        if size_specified:
            rows = self._translate_data_value(level_data['size'][1])
            cols = self._translate_data_value(level_data['size'][0])

        # Load layers
        level_layers = []
        self.layer_dict = {} # TODO Temporary method of accessing layers by title
        for layer_data in level_data['layers']:
            graphic_data = layer_data['graphic_data']

            # TODO Try using map() for this
            for data_property, data_value in graphic_data.iteritems():
                graphic_data[data_property] = self._translate_data_value(data_value)

            if 'layer_data' in layer_data:
                # TODO Try using map() for this
                for data_property, data_value in layer_data['layer_data'].iteritems():
                    layer_data['layer_data'][data_property] = self._translate_data_value(data_value)

            # Drop in the key_handler object if necessary
            if 'key_handler' in graphic_data:
                graphic_data['key_handler'] = key_handler

            # TODO Remove the need for this hotfix
            # Get the tiles from the stage layer for the character
            if 'stage_layer' in graphic_data:
                # TODO Should just pass a reference to the stage or something here instead of having this class be aware of what to do
                graphic_data['stage'] = self.layer_dict[graphic_data['stage_layer']].graphic.tiles
                del graphic_data['stage_layer']

            layer_graphic = create_graphics_object(self._translate_data_value(layer_data['graphic_type']), **graphic_data)

            # TODO Remove the need for this hotfix
            if self._translate_data_value(layer_data['title']) == 'player':
                layer_graphic = layer_graphic.character

            if 'layer_data' in layer_data:
                layer = layers.create_from(layer_graphic, **layer_data['layer_data'])
            else:
                layer = layers.create_from(layer_graphic)

            if self._translate_data_value(level_data['camera_target']) == layer_data['title']:
                camera_target = layer.graphic

            level_layers.append(layer)
            self.layer_dict[self._translate_data_value(layer_data['title'])] = layer

        # TODO If the size isn't specified, an unbounded camera should be used in place of this hotfix
        if not size_specified:
            rows = cols = 1000

        stage_boundary = BoundedBox(0, 0, cols*TILE_SIZE, rows*TILE_SIZE)
        # TODO Don't hardcode window size, make it a global setting
        self.camera = viewport.Camera(0, 0, 800, 600, bounds=stage_boundary, target=camera_target)
        self.camera.focus() # TODO Should this be called on init?

        self.layer_manager = layers.LayerManager(self.camera, level_layers)

    def _translate_data_value(self, data_value):
        """Translates tagged data value strings to their intended values."""
        # TODO Process tags from right to left to allow for chaining
        # TODO Move these tags to the appropriate classes
        tags = {
            tag_prefix+'tileset'+tag_suffix: Tileset.load,
            tag_prefix+'tilemap'+tag_suffix: load_tile_map,
        }

        # If the data value is a string, it could contain a tag
        if isinstance(data_value, basestring):
            for tag, translation in tags.iteritems():
                if data_value[0:len(tag)] == tag:
                    # Translate the data value without the tag prepended
                    return translation(data_value[len(tag):])

        return data_value

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
    def add_config_data_translator(cls, data_type, translator):
        """Adds a support for translating data strings of the given data type when
        loading a level config. All string values tagged with this data type will be
        run through the translator.

        Args:
            data_type (string): The name of the data type to add translation support for.
                                This will be the tag to signify that a string should have
                                the translator applied to it.
            translator (function): The function to apply to all tagged data values.
        """
        self._installed_translators[self._data_value_tag_prefix+data_type+self._data_value_tag_suffix] = translator

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
