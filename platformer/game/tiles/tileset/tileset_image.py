from pyglet.image import ImageGrid, TextureGrid
from ...settings.general_settings import TILE_SIZE
from math import ceil

class TilesetImage(object):
	"""Tileset image data which defines how each tile in a tileset should look.

	Tileset images can be gif, png, or jpg, and should be drawn
	with a grid in mind.

	Tileset image files should have the filename "tiles" and be
	located in a tileset subdirectory. An example path would be
	``{resources_dir}/{tilesets_dir}/{tileset_name}/tiles.gif``.

	Attributes:
		rows (int): The number of rows of tiles in the tileset image.
		cols (int): The number of columns of tiles in the tileset image.
	"""

	def __init__(self, tileset_image, rows=None, cols=None):
		"""Manages the images for tiles in a tileset.

		The number of rows and columns of tiles in the file can
		optionally be specified.

		Args:
			tileset_image (:class:`pyglet.image.Texture`): The tileset image containing all tiles.

		Kwargs:
			rows (int): The number of rows of tiles in the tileset image.
			cols (int): The number of columns of tiles in the tileset image.
		"""
		# If rows and columns were not specified, calculate them
		if not rows:
			rows = int(ceil(tileset_image.height / TILE_SIZE))
		if not cols:
			cols = int(ceil(tileset_image.width / TILE_SIZE))

		self._image = TextureGrid(ImageGrid(tileset_image, rows, cols))
		self._image_data = {}
		self.rows = rows
		self.cols = cols

	def _value_to_indices(self, tile_value):
		"""Converts a numeric tile value to an index in the tileset image grid.

		Args:
			tile_value (int): The integer value of a tile in the tileset.

		Returns:
			A tuple of the tile value's coordinates in the tile image formatted as ``(col, row)``.
		"""
		row = (tile_value - 1) / self.cols
		col = tile_value - (row * self.cols) - 1
		row = self.rows - row - 1 # Adjust for index 0 being at the bottom left

		return (row, col)

	def get_tile_image(self, tile_value):
		"""Returns the image for a tile in the tileset.

		Args:
			tile_value (int): The integer value of a tile in the tileset.

		Returns:
			A :class:`pyglet.image.Texture` object of the tile's image.
		"""
		indices = self._value_to_indices(tile_value)
		return self._image[indices[0], indices[1]]

	def get_tile_image_data(self, tile_value):
		"""Returns the image data for a tile in the tileset.

		Image data retrieval calls are cached after the first access
		to improve performance.

		Args:
			tile_value (int): The integer value of a tile in the tileset.

		Returns:
			A :class:`pyglet.image.ImageData` object for the tile's image data.
		"""
		# If the image data for this tile is not cached, cache it
		if not tile_value in self._image_data:
			self._image_data[tile_value] = self.get_tile_image(tile_value).get_image_data()

		return self._image_data[tile_value]
