from basic_animation import BasicAnimation
from pyglet.image import TileableTexture

class TiledAnimation(BasicAnimation):
	"""An animation which can be tiled efficiently.

	Attributes:
		width (number): The width of the tiled animation.
		height (number): The height of the tiled animation.
	"""

	def __init__(self, frames, width, height, *args, **kwargs):
		"""Creates a new tileable animation.

		Args:
			frames (list of :class:`game.animation.animation_frame.AnimationFrame`): The frames that make up the animation.
			width (number): The width of the tiled animation.
			height (number): The height of the tiled animation.
		"""
		super(TiledAnimation, self).__init__(frames, *args, **kwargs)
		self.width = width
		self.height = height

	def draw(self, x=0, y=0):
		self.current_frame.image.blit_tiled(x, y, 0, self.width, self.height)

	@staticmethod
	def _create_animation_frame_image(image):
		return TileableTexture.create_for_image(image)
