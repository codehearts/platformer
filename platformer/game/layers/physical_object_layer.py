import sprite_layer

class PhysicalObjectLayer(sprite_layer.SpriteLayer):
	# TODO Upate path of class name in docstring
	"""A layer which contains a :class:`physical_objects.physicalobject.PhysicalObject` as its content.

	This layer does not call :func:`update` on the given :class:`physical_objects.physicalobject.PhysicalObject`
	"""

	def __init__(self, *args, **kwargs):
		super(PhysicalObjectLayer, self).__init__(*args, **kwargs)

	def update(self, dt):
		pass
