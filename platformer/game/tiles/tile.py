from game.extended_sprite import ExtendedSprite

# TODO Does this really need to subclass Sprite? Does this really need access to the image?
# TODO Possibly have a large tiling tile class which can be used to draw large regions of repeated tiles with a single tile object
# TODO Possible have a class for drawing large tiles with multiple artworks/a slice of the tileset image for an image
class Tile(ExtendedSprite):
	"""A tile for use in maps.

	Attributes:
		is_collidable (bool): Whether the tile can be collided with.
		type (str): The type of tile.
	"""

	type = 'basic'

	def __init__(self, *args, **kwargs):
		"""Creates a new tile.

		Kwargs:
			is_collidable (bool): Whether the tile can be collided with.
		"""
		self.is_collidable = kwargs.pop('is_collidable', True)

		super(Tile, self).__init__(*args, **kwargs)

	def resolve_collision_x(self, obj):
		"""Resolves a collision with a physical object on the x-axis.

		Args:
			obj (:class:`game.physical_objects.physical_object.PhysicalObject`): The physical object to resolve a collision with.

		Returns:
			True if a collision occurred, False otherwise.
		"""
		# If the object is moving left
		if obj.moving_to_x < obj.x:
			obj.moving_to_x = self.x2
			obj.on_left_collision(self)

			return True
		# If the object is moving right
		else:
			obj.moving_to_x = self.x - obj.width
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
		if obj.moving_to_y < obj.y:
			# Move it on top of the tile
			obj.moving_to_y = self.y2
			obj.on_bottom_collision(self)

			return True
		# If the object is moving up from below the tile
		elif obj.moving_to_y < self.y2:
			# Move it under the tile
			obj.moving_to_y = self.y - obj.height
			obj.on_top_collision(self)

			return True

		return False
