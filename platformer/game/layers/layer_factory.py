from ..animation.basic_animation import BasicAnimation
from ..physical_objects.physicalobject import PhysicalObject
from ..text.text import Text
from . import *
from pyglet.sprite import Sprite

def create_layer(graphic, *args, **kwargs):
	"""Creates the appropriate layer object for the given graphic and style specifications.

	Please see the documentation for :class:`game.layers.basic_layer.BasicLayer` for a
	full list of arguments that can be passed to this method.

	Args:
		graphic (object): The graphic to be drawn on the layer.

	Kwargs:
		fixed (bool): Whether the layer should be fixed relative to the viewport or not.

	Returns:
		A layer object.
	"""
	fixed = kwargs.pop('fixed', False)

	if isinstance(graphic, PhysicalObject):
		layer_type = PhysicalObjectLayer
	elif isinstance(graphic, Sprite):
		if fixed:
			layer_type = FixedSpriteLayer
		else:
			layer_type = SpriteLayer
	# TODO Support TileMap and fixed TileMap
	#elif isinstance(graphic, TileMap):
		#if fixed:
			#layer_type = FixedTileMapLayer
		#else:
			#layer_type = TileMapLayer
	elif isinstance(graphic, Text):
		if fixed:
			layer_type = FixedTextLayer
		else:
			layer_type = TextLayer
	elif isinstance(graphic, BasicAnimation):
		if fixed:
			layer_type = FixedAnimationLayer
		else:
			layer_type = AnimationLayer
	else:
		if fixed:
			layer_type = FixedLayer
		else:
			layer_type = BasicLayer

	return layer_type(graphic, *args, **kwargs)
