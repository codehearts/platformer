from base_layer import BaseLayer
from installed_layers import installed_layers

def create_from(graphic, *args, **kwargs):
	"""Creates a layer for the given graphic and style specifications.

	In addition to this method's arguments, the layer's arguments should
	be passed as well.

	This factory will only return types that have been installed via the
	installed_layers module.

	Args:
		graphic (object): The graphic to be drawn on the layer.

	Kwargs:
		static (bool): Whether the layer should be updated.
		fixed (bool): Whether the layer should be fixed relative to the viewport.

	Returns:
		A layer object.
	"""
	global installed_layers
	fixed = kwargs.pop('fixed', False)
	static = kwargs.pop('static', False)

	layer_type = BaseLayer
	for layer in installed_layers:
		if layer['recognizer'](graphic):
			layer_type = layer['factory'](static=static, fixed=fixed)
			break

	return layer_type(graphic, *args, **kwargs)
