from pyglet.resource import file as open_resource_file
from game.tiles import Tileset
from ..settings.general_settings import LEVEL_DIRECTORY, LEVEL_FORMAT

# TODO Level loader tests
class Level(object):
    # TODO Set up the level

    def __init__(self, level_data):
        """Loads a level from disk.

        Args:
                level_data (dict): A dictionary of level parameters.
        """
        # TODO Initialize the level objects from the given data
        self.title = level_data['title']

        """
        # TODO Load each tileset into an array, and have the data file sepcify which tileset to use per layer
        tilesets = {} #TODO Use a dict for this
        for tileset in level_data.tilesets:
            tilesets[tileset] = Tileset.load(tileset)
        """

        for layer in level_data['layers']:
            if 'tileset'

    @classmethod
    def load(cls, level_title):
        # TODO The game.level.Level class in the doc should be updated once this class is finalized
        """Loads a level from a given level title.

        Args:
                level_title (str): The title of the level to load.

        Returns:
                A :class:`game.level.Level` object.
        """
        level_file = open_resource_file(LEVEL_DIRECTORY+'/'+level_name+'.'+LEVEL_FORMAT)

        # TODO Load the level data from the file, pass it to the init function

        return cls(level_data)
