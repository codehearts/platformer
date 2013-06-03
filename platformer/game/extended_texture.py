from bounded_box import BoundedBox
from pyglet.image import Texture, TextureRegion

class ExtendedTexture(BoundedBox, Texture):
	""":class:`pgylet.image.Texture` which tracks its dimensions in terms of pixels and tiles."""

	def __init__(self, width, height, *args, **kwargs):
		BoundedBox.__init__(self, 0, 0, width, height)
		Texture.__init__(self, width, height, *args, **kwargs)

		self.region_class = ExtendedTextureRegion

class ExtendedTextureRegion(BoundedBox, TextureRegion):
	""":class:`pyglet.image.TextureRegion` which tracks its dimensions in terms of pixels and tiles."""

	def __init__(self, x, y, z, width, heigth, *args):
		BoundedBox.__init__(self, x, y, width, heigth)
		TextureRegion.__init__(self, x, y, z, width, heigth, *args)
