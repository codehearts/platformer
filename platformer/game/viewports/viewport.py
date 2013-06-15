from game.bounded_box import BoundedBox

class Viewport(BoundedBox):

	def __init__(self, *args, **kwargs):
		"""
		Kwargs:
			bounds (BoundedBox): Limit the position of the viewport to within these bounds.
		"""
		self.bounds = kwargs.pop('bounds', None)

		super(Viewport, self).__init__(*args, **kwargs)
