from tileset_config import TilesetConfig
from tileset_image import TilesetImage
from loader import get_tileset_config, get_tileset_image
from .. import tile_factory

# TODO Instead of loading the data itself, the data could be loaded by the loader file and then this class would be more testable because it doesn't require files
class Tileset(object):
	"""Loads and manages the appearance and behavoir of tiles in a tileset.

	A tileset is an image file containing multiple tile artworks and an
	optional config file specifying the behavior of those tiles. Tilesets
	are located in their own subdirectories of
	``{resources_dir}/{tilesets_dir}/`` such as
	``{resources_dir}/{tilesets_dir}/forest/``, for example.

	Attributes:
		image (:class:`game.tiles.tileset.tileset_image.TilesetImage`): The image data for the tileset.
		config (:class:`game.tiles.tileset.tileset_config.TilesetConfig`): The config data for the tileset.
	"""

	_cached_tilesets = {}

	def __init__(self, tileset_name, rows=None, cols=None):
		"""Loads a new tileset and manages its image and config data.

		Args:
			tileset_name (str): The name of the tileset.

		Kwargs:
			rows (int): The number of rows of tiles in the tileset image.
			cols (int): The number of columns of tiles in the tileset image.
		"""
		if not tileset_name in self._cached_tilesets:
			self._cache_tileset(tileset_name, rows, cols)

		self.image = self._cached_tilesets[tileset_name]['image']
		self.config = self._cached_tilesets[tileset_name]['config']

	def _cache_tileset(self, tileset_name, rows, cols):
		"""Caches a tileset.

		Args:
			tileset_name (str): The name of the tileset.
			rows (int): The number of rows of tiles in the tileset image.
			cols (int): The number of columns of tiles in the tileset image.
		"""
		self._cached_tilesets[tileset_name] = {}

		self._cached_tilesets[tileset_name]['image'] = TilesetImage(get_tileset_image(tileset_name), rows, cols)
		self._cached_tilesets[tileset_name]['config'] = TilesetConfig(get_tileset_config(tileset_name))

	def create_tile(self, tile_value, *args, **kwargs):
		"""Creates a tile object for the given tile value in the tileset.

		The arguments for the tile object should be passed when
		calling this method.

		Args:
			tile_value (int): The integer value of a tile in the tileset.

		Returns:
			The appropriate :class:`game.tiles.tile.Tile` object for the given tile value.
		"""
		# Merge the keyword arguments with any additional arguments from the tileset config
		kwargs = dict(kwargs.items() + self.config.get_tile_entry(tile_value).items())

		return tile_factory.create_tile(img=self.image.get_tile_image(tile_value), *args, **kwargs)
