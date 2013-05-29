class AnimationFrame(object):
	"""A single frame of an animation."""

	def __init__(self, image, duration):
		"""Creates an animation frame from an image.

		Args:
			image (object): The image of this frame.
			duration (number): Number of seconds to display the frame, or ``None`` if it is the last frame in the animation.
		"""
		self.image = image
		self.duration = duration
