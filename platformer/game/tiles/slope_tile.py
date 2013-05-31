# -*- coding: utf-8 -*-

import tile
import math
from ..settings import general_settings

class _SlopeTile(tile.Tile):
	"""A sloped tile for use in maps.

	Attributes:
		left_height (int): The height of the left end of the slope.
		right_height (int): The height of the right end of the slope.
		faces_left (bool): Whether the face of the slopes faces left.
		faces_right (bool): Whether the face of the slopes faces right.
		is_ceiling (bool): Whether this slope is intended for use as a ceiling tile.
	"""

	def __init__(self, left_height, right_height, *args, **kwargs):
		"""Creates a new slope tile.

		Args:
			left_height (int): The height of the left end of the slope.
			right_height (int): The height of the right end of the slope.
		"""
		super(_SlopeTile, self).__init__(*args, **kwargs)

		self.left_height = int(left_height)
		self.right_height = int(right_height)
		self.faces_left = False
		self.faces_right = False
		self.is_ceiling = False

		self.type = 'slope'

	def resolve_collision_y(self, obj):
		if not self.is_collidable:
			return False

		# If the object is moving down
		if obj.moving_to_y < obj.hitbox.y:
			# TODO Clean up this method!
			# Position on the tile, from the center of this object (0 is left, 1 is right)
			position_on_tile = (obj.hitbox.x + obj.hitbox.half_width - self.x) / general_settings.TILE_SIZE_FLOAT

			if position_on_tile < 0:
				slope_y = self.left_height
			elif position_on_tile > 1:
				slope_y = self.right_height
			else:
				slope_y = int(math.ceil((1-position_on_tile)*self.left_height + position_on_tile*self.right_height))

			slope_y += self.y

			# TODO Determine whether the player is falling above the slope or just came from another connected slope, and set in_air accordingly
			# TODO A constant value is not the right way to determine if we fell onto the slope or not
			#if obj.hitbox.y - 5 > slope_y:
				## TODO Set is_falling somehow, not just in_air
				#obj.in_air = True

			# If we're on the ground or we're colliding with the slope, register the collision
			if not obj.in_air or obj.moving_to_y <= slope_y:
				obj.moving_to_y = slope_y
				obj.on_bottom_collision()

				return True
		# TODO A constant value is not a good way of handling this
		elif obj.hitbox.y2 - self.y < 5:
			# @TODO This check is no good and allows you to move through slopes from below diagonally
			# Collide with the bottoms of slope tiles
			# A threshold of 5 pixels ensures that we don't collide with other tiles on a multi-tile slope when jumping
			obj.moving_to_y = self.y - obj.hitbox.height
			obj.on_top_collision(self)

			return True

		return False

class LeftwardSlopeTile(_SlopeTile):
	"""A sloped floor tile which faces to the left (◢)."""

	def __init__(self, *args, **kwargs):
		super(LeftwardSlopeTile, self).__init__(*args, **kwargs)

		self.faces_left = True

	# TODO Probably don't need tile_map kwarg
	def resolve_collision_x(self, obj):
		if not self.is_collidable:
			return False

		# If the object is moving left
		# TODO Comment this better
		# TODO self.y + self.right_height could be cached, but needs to be updated if self.y is ever changed
		# TODO Clean up this mess, probably by writing utility methods to make this more readable
		if obj.hitbox.x >= self.x2 and obj.hitbox.y < self.y + self.right_height and obj.moving_to_x < obj.hitbox.x:
			obj.moving_to_x = self.x2
			return True
		if obj.hitbox.x2 <= self.x and obj.hitbox.y < self.y and obj.hitbox.y2 >= self.y and obj.moving_to_x > obj.hitbox.x:
			obj.moving_to_x = self.x - obj.hitbox.width
			return True

		return False

class RightwardSlopeTile(_SlopeTile):
	"""A sloped floor tile which faces to the right (◣)."""

	def __init__(self, *args, **kwargs):
		super(RightwardSlopeTile, self).__init__(*args, **kwargs)

		self.faces_right = True

	def resolve_collision_x(self, obj, tile_map=None):
		if not self.is_collidable:
			return False

		# TODO Comment this better
		# TODO self.y + self.right_height could be cached, but needs to be updated if self.y is ever changed
		# TODO Clean up this mess, probably by writing utility methods to make this more readable
		if obj.hitbox.x2 <= self.x and obj.hitbox.y < self.y + self.left_height and obj.moving_to_x > obj.hitbox.x:
			obj.moving_to_x = self.x - obj.hitbox.width
			return True
		if obj.hitbox.x >= self.x2 and obj.hitbox.y < self.y and obj.hitbox.y2 >= self.y and obj.moving_to_x < obj.hitbox.x:
			obj.moving_to_x = self.x2
			return True

		return False

# TODO Implement this
class LeftwardCeilingSlopeTile(_SlopeTile):
	"""A sloped ceiling tile which faces to the left (◥)."""

	def __init__(self, *args, **kwargs):
		super(LeftwardCeilingSlopeTile, self).__init__(*args, **kwargs)

		self.faces_left = True
		self.is_ceiling = True

# TODO Implement this
class RightwardCeilingSlopeTile(_SlopeTile):
	"""A sloped ceiling tile which faces to the left (◤)."""

	def __init__(self, *args, **kwargs):
		super(RightwardCeilingSlopeTile, self).__init__(*args, **kwargs)

		self.faces_right = True
		self.is_ceiling = True
