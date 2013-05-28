import sprite_layer

class PhysicalObjectLayer(sprite_layer.SpriteLayer):
	# TODO The class path in the docstring has probably changed
	"""A layer which contains a :class:`game.physical_objects.physical_object.PhysicalObject` as its content.

	This layer does not call :func:`update` on the given :class:`game.physical_objects.physical_object.PhysicalObject`.
	"""

	def __init__(self, *args, **kwargs):
		super(PhysicalObjectLayer, self).__init__(*args, **kwargs)

	# Remove the inherited update method from this class
	update = property()
