import tile

class SlopeTile(tile.Tile):
	def __init__(self, left_height, right_height, *args, **kwargs):
		"""

		Kwargs:
			is_ceiling (bool): Whether this slope tile is intended for use as ceiling.
		"""
		self.is_ceiling = kwargs.pop('is_ceiling', False)

		super(SlopeTile, self).__init__(*args, **kwargs)

		self.type = 'slope'
		self.is_rightward = False
		self.is_leftward = False
		self.slope_pieces = None # TODO Why is this a float?
		self.left_height = None
		self.right_height = None

# TODO Ceiling slope tiles
