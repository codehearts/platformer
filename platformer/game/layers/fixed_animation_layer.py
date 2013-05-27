import animation_layer

# TODO Should support automatic layer deletion when the animation ends as a setting
class FixedAnimationLayer(animation_layer.AnimationLayer):
	"""A layer of animated graphical content which remains fixed relative to the viewport."""

	def __init__(self, *args, **kwargs):
		"""
		Kwargs:
			offset_x (number): The number of pixels to horizontally offset the graphical content from the viewport's anchor point (usually the bottom left corner).
			offset_y (number): The number of pixels to vertically offset the graphical content from the viewport's anchor point (usually the bottom left corner).
		"""
		# Get this subclass's kwargs, or their default value if they were not specified
		# Calling kwargs.pop means they won't be present when initializing the parent
		self.offset_x = kwargs.pop('offset_x', 0)
		self.offset_y = kwargs.pop('offset_y', 0)

		super(FixedAnimationLayer, self).__init__(*args, **kwargs)

	def draw(self):
		self.graphic.draw(self.viewport.x + self.offset_x, self.viewport.y + self.offset_y)
