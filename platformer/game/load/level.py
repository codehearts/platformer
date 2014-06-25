from pyglet.resource import file as open_resource_file
from game.graphics import create_graphics_object
from game import layers
from json import load as json_load
from ..settings.general_settings import RESOURCE_PATH, LEVEL_DIRECTORY, LEVEL_FORMAT
import game.scripts

class Level(object):
	"""Contains the layers, viewport, and scripts for a level.
	The level can be loaded from a config file in the resources/levels directory by calling
	`Level.load` with the level file's name. All layers, scripts, and the viewport will be
	initialized and loaded.

	Static Properties:
		current_processing_layer (str): The title of the layer currently being processed, or None
		                                if no processing is being performed. Useful for translators.
		current_processed_layers (dict): Layers which have already been processed as layer_title: layer_object.
		                                 The dict will be empty if processing is not currently ongoing.

	Properties:
		camera (:class:`viewport.Viewport`): The camera for the level.
		layer_manager (:class:`layers.LayerManager`): The layer manager for the level's layers.
	"""

	# The title of the layer currently being processed
	current_processing_layer = None
	# Dictionary of layers which have already been processed, as layer_title: layer_object
	current_processed_layers = {}

	def __init__(self, level_data):
		"""Loads a level from disk.

		Args:
			level_data (dict): A dictionary of level parameters.
		"""
		# TODO Implement ability to specify whether to load a script before the level is loaded or after
		# Scripts must be loaded first because they provide dynamic values which may be used
		if 'scripts' in level_data:
			game.scripts.load_custom_scripts(config_translators.translate(level_data['scripts']))

		# Translate all level data values, without recursing because we'll translate the layer data individually
		level_data = config_translators.translate(level_data, recurse=False)

		# Check if the boundaries of the map were specified
		if 'size' in level_data:
			level_data['size'] = config_translators.translate(level_data['size'])
			rows = level_data['size']['rows']
			cols = level_data['size']['cols']
		else:
			# TODO If the size isn't specified, an unbounded camera should be used in place of this hotfix
			rows = cols = 1000

		# Loop through layers, keeping track of the current processing layer
		for layer_index, layer_config in enumerate(level_data['layers']):
			Level.current_processing_layer = config_translators.translate(layer_config['title'])
			level_data['layers'][layer_index] = config_translators.translate(layer_config)

		Level.current_processing_layer = None
		level_data['viewport'] = config_translators.translate(level_data['viewport'])

		# Enable post processing of level config data
		config_translators.enable_post_processing()

		# Post-process the level config and create the layers
		initialized_layers = []
		while len(initialized_layers) != len(level_data['layers']):
			for layer_index, layer_config in enumerate(level_data['layers']):
				Level.current_processing_layer = config_translators.translate(layer_config['title'])

				# Skip layers that still have unmet dependencies or have already been processed
				if not config_translators.ready_for_translation(Level.current_processing_layer) or Level.current_processing_layer in Level.current_processed_layers:
					continue

				# Translate all layer data values
				layer_config = config_translators.translate(level_data['layers'][layer_index])

				graphic_type = layer_config['graphic']['type']
				del layer_config['graphic']['type'] # Remove the graphic type from the graphic arguments

				layer_graphic = create_graphics_object(graphic_type, **layer_config['graphic'])

				# TODO Remove the need for this hotfix
				if Level.current_processing_layer == 'player':
					layer_graphic = layer_graphic.character

				# Add the layer title as an argument for creating the layer
				if not 'layer' in layer_config:
					layer_config['layer'] = {'title': self.current_processing_layer}
				else:
					layer_config['layer']['title'] = self.current_processing_layer

				layer = layers.create_from(layer_graphic, **layer_config['layer'])

				initialized_layers.append(layer)
				Level.current_processed_layers[Level.current_processing_layer] = layer

		# Clean ip the static properties once loading is finished
		Level.current_processing_layer = None

		# Create the viewport
		level_data['viewport'] = config_translators.translate(level_data['viewport'])
		graphic_type = level_data['viewport']['type']
		del level_data['viewport']['type'] # Remove the graphic type from the graphic arguments

		viewport = create_graphics_object(graphic_type, **level_data['viewport'])

		# Disable post processing of level config data so more levels can be loaded
		config_translators.disable_post_processing()

		# Initialize the layer manager
		self.layer_manager = layers.LayerManager(viewport, initialized_layers)

		# Clean ip the static properties once loading is finished
		Level.current_processed_layers = {}

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

# Import at bottom to resolve circular dependency
import config_translators
