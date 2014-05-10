from basic_animation import BasicAnimation
from game.graphics import install_graphics_module
from pyglet.image import TileableTexture

class TiledAnimation(BasicAnimation):
	"""An animation which can be tiled efficiently.

        A TiledAnimation object can be created by the graphics
        factory by specifying "tiled animation" as the graphics type.

	Attributes:
		width (int): The width of the tiled animation.
		height (int): The height of the tiled animation.
	"""

	def __init__(self, frames, width, height, *args, **kwargs):
		"""Creates a new tileable animation.

		Args:
			frames (list of :class:`game.animation.AnimationFrame`): The frames that make up the animation.
			width (int): The width of the tiled animation.
			height (int): The height of the tiled animation.
		"""
		super(TiledAnimation, self).__init__(frames, *args, **kwargs)
		self.width = int(width)
		self.height = int(height)

	def blit(self, x, y):
		self.current_frame.image.blit_tiled(x, y, 0, self.width, self.height)

	@staticmethod
	def _create_animation_frame_image(image):
		return TileableTexture.create_for_image(image)



def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.animation.TiledAnimation`."""
	return graphics_type == 'tiled animation'

def factory(*args, **kwargs):
	"""Returns a :class:`game.animation.TiledAnimation` for the given arguments."""
	return TiledAnimation.from_image(*args, **kwargs)

install_graphics_module(__name__)
