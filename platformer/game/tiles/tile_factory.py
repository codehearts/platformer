from tile import Tile
from slope_tile import RightwardSlopeTile, LeftwardSlopeTile, RightwardCeilingSlopeTile, LeftwardCeilingSlopeTile

# TODO Each tile class should be able to hook in a method to determine if the given tile is right for it
def create_tile(*args, **kwargs):
	"""Creates the appropriate tile object for the given tile data.

	Returns:
		A tile object.
	"""
	tile_type = kwargs.pop('type', None)

	# TODO Make these checks more extensible
	# Check for slope
	if tile_type is 'slope':
		# Check for not ceiling slope
		is_ceiling = kwargs.pop('is_ceiling', False)
		if not is_ceiling:
			# Check for rightward facing slope
			if kwargs['left_height'] > kwargs['right_height']:
				return RightwardSlopeTile(*args, **kwargs)
			else:
				return LeftwardSlopeTile(*args, **kwargs)
		else:
			# Check for leftward facing slope
			if kwargs['left_height'] > kwargs['right_height']:
				return LeftwardCeilingSlopeTile(*args, **kwargs)
			else:
				return RightwardCeilingSlopeTile(*args, **kwargs)

	return Tile(*args, **kwargs)
