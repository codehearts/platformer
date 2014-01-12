from pyglet.resource import file as open_resource_file
from ..settings.general_settings import LEVEL_DIRECTORY, LEVEL_FORMAT

class load_level(level_data):
	# TODO Set up the level

	def __init__(self, level_name):
            level_file = open_resource_file(LEVEL_DIRECTORY+'/'+level_name+'.'+LEVEL_FORMAT)
