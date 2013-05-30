from pyglet.sprite import Sprite
from settings.general_settings import TILE_SIZE

# TODO Implement this
class Tile(Sprite):
	"""A tile for use in maps.

	Attributes:
		x2 (int): The x coordinate of a point opposite the tile's anchor point (usually the bottom left corner).
		y2 (int): The y coordinate of a point opposite the tile's anchor point (usually the bottom left corner).
		tile_x (int): The x coordinate of the tile in terms of tiles (as opposed to pixels).
		tile_y (int): The y coordinate of the tile in terms of tiles (as opposed to pixels).
		collidable (bool): Whether the tile can be collided with.
	"""

	def __init__(self, *args, **kwargs):
		"""Creates a new tile.

		Kwargs:
			collidable (bool): Whether the tile can be collided with.
		"""
		self.collidable = kwargs.pop('collidable', True)

		super(Tile, self).__init__(*args, **kwargs)

		# Set the position as an integer for optimal rendering
		self.x = int(self.x)
		self.y = int(self.y)
		self.x2 = self.x + int(self.width)
		self.y2 = self.y + int(self.height)

		# Get the coordinates in terms of tiles
		self.tile_x = self.x / TILE_SIZE
		self.tile_y = self.y / TILE_SIZE

		self.type = 'basic'
