from game.load.level import Level

# Dictionary of layers and their layer graphic dependencies
_layer_graphic_dependencies = {}

def _layer_dependencies_met(layer_title):
	"""Returns True if the given layer has had its dependencies met, or False otherwise.

	Args:
	layer_title (str): The name of the layer to check the dependencies of.
	"""
	if layer_title in _layer_graphic_dependencies:
		return reduce(lambda x,y: x and (y in Level.current_processed_layers), _layer_graphic_dependencies[layer_title], True)
	return True

def _register_layer_graphic_dependency(property_name):
	"""Marks the currently processed layer as depending on the graphic from another layer.
	This is done by returning the property value with a translation tag for obtaining that
	layer graphic during post-processing.
	"""
	split = property_name.find('.')
	dependecy_layer_title = property_name[ : split]

	if not Level.current_processing_layer in _layer_graphic_dependencies:
		_layer_graphic_dependencies[Level.current_processing_layer] = [dependecy_layer_title]
	else:
		_layer_graphic_dependencies[Level.current_processing_layer].append(dependecy_layer_title)

	# TODO There should be a way for this method to tell the translator to stop translating tags for this property after this one
	return '::resolve_layer_graphic_dependency::' + property_name

def _get_layer_graphic_property(property_name):
	"""Returns the specified layer graphic property. This must be done during post-processing."""
	split = property_name.find('.')
	layer_title = property_name[ : split]

	# Remove the layer from the list of layer dependencies
	_layer_graphic_dependencies[Level.current_processing_layer].remove(layer_title)

	return getattr(Level.current_processed_layers[layer_title].graphic, property_name[split + 1 : ])
