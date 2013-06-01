from pyglet.sprite import Sprite
from ..settings.general_settings import TILE_SIZE

class Tile(Sprite):
	"""A tile for use in maps.

	Attributes:
		x (int): The x coordinate of the tile's anchor point (usually the bottom left corner)
		y (int): The y coordinate of the tile's anchor point (usually the bottom left corner)
		x2 (int): The x coordinate of a point opposite the tile's anchor point (usually the bottom left corner).
		y2 (int): The y coordinate of a point opposite the tile's anchor point (usually the bottom left corner).
		tile_x (int): The x coordinate of the tile in terms of tiles (as opposed to pixels).
		tile_y (int): The y coordinate of the tile in terms of tiles (as opposed to pixels).
		is_collidable (bool): Whether the tile can be collided with.
		type (str): The type of tile.
	"""

	def __init__(self, *args, **kwargs):
		"""Creates a new tile.

		Kwargs:
			is_collidable (bool): Whether the tile can be collided with.
		"""
		self.is_collidable = kwargs.pop('is_collidable', True)

		super(Tile, self).__init__(*args, **kwargs)

		# Set the position as an integer for optimal rendering
		self.x = int(self.x)
		self.y = int(self.y)
		self.x2 = self.x + int(self.width)
		self.y2 = self.y + int(self.height)

		# Get the coordinates in terms of tiles
		self.tile_x = self.x / TILE_SIZE
		self.tile_y = self.y / TILE_SIZE

		# TODO I don't like this being a string comparison
		self.type = 'basic'

	def resolve_collision_x(self, obj):
		"""Resolves a collision with a physical object on the x-axis.

		Args:
			obj (:class:`game.physical_objects.physical_object.PhysicalObject`): The physical object to resolve a collision with.

		Returns:
			True if a collision occurred, False otherwise.
		"""
		# If the object is moving left
		if obj.moving_to_x < obj.hitbox.x:
			obj.moving_to_x = self.x2
			obj.on_left_collision(self)

			return True
		# If the object is moving right
		else:
			obj.moving_to_x = self.x - obj.hitbox.width
			obj.on_right_collision(self)

			return True

	def resolve_collision_y(self, obj):
		"""Resolves a collision with a physical object on the y-axis.

		Args:
			obj (:class:`game.physical_objects.physical_object.PhysicalObject`): The physical object to resolve a collision with.

		Returns:
			True if a collision occurred, False otherwise.
		"""
		# If the object is moving down through the tile
		if obj.moving_to_y < obj.hitbox.y:
			# Move it on top of the tile
			obj.moving_to_y = self.y2
			obj.on_bottom_collision(self)

			return True
		# If the object is moving up from below the tile
		elif obj.moving_to_y < self.y2:
			# Move it under the tile
			obj.moving_to_y = self.y - obj.hitbox.height
			obj.on_top_collision(self)

			return True

		return False
