from bounded_box import BoundedBox
from pyglet.sprite import Sprite

class ExtendedSprite(BoundedBox, Sprite):
	""":class:`pgylet.sprite.Sprite` which tracks its dimensions in terms of pixels and tiles."""

	def __init__(self, img, *args, **kwargs):
		Sprite.__init__(self, img, *args, **kwargs)
		BoundedBox.__init__(self, self.x, self.y, img.width, img.height)
