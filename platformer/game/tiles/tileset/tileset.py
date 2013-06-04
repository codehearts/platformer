from tileset_config import TilesetConfig
from tileset_image import TilesetImage
from loader import get_tileset_config, get_tileset_image
from .. import tile_factory

class Tileset(object):
	"""Manages the appearance and behavior of tiles in a tileset.

	A tileset is an image file containing multiple tile artworks and an
	optional config file specifying the behavior of those tiles. Tilesets
	are located in their own subdirectories of
	``{resources_dir}/{tilesets_dir}/`` such as
	``{resources_dir}/{tilesets_dir}/forest/``, for example.

	Attributes:
		name (str): The name of the tileset.
		image (:class:`game.tiles.tileset.TilesetImage`): The image data for the tileset.
		config (:class:`game.tiles.tileset.TilesetConfig`): The config data for the tileset.
	"""

	_cached_tilesets = {}

	def __init__(self, tileset_name, tileset_image, tileset_config):
		"""Manages the tile images and config data for a tileset.

		Args:
			tileset_name (str): The name of the tileset.
			tileset_image (:class:`game.tiles.tileset.TilesetImage`): The image data for the tileset.
			tileset_config (:class:`game.tiles.tileset.TilesetConfig`): The config data for the tileset.
		"""
		if not tileset_name in self._cached_tilesets:
			self._cache_tileset(tileset_name, tileset_image, tileset_config)

		# Update the cache if necessary
		if tileset_image != self._cached_tilesets[tileset_name]['image']:
			self._cached_tilesets[tileset_name]['image'] = tileset_image
		if tileset_config != self._cached_tilesets[tileset_name]['config']:
			self._cached_tilesets[tileset_name]['config'] = tileset_config

		self.name = tileset_name
		self.image = self._cached_tilesets[tileset_name]['image']
		self.config = self._cached_tilesets[tileset_name]['config']

	@classmethod
	def _cache_tileset(cls, tileset_name, tileset_image, tileset_config):
		"""Caches a tileset.

		Args:
			tileset_name (str): The name of the tileset.
			tileset_image (:class:`game.tiles.tileset.TilesetImage`): The image data for the tileset.
			tileset_config (:class:`game.tiles.tileset.TilesetConfig`): The config data for the tileset.
		"""
		cls._cached_tilesets[tileset_name] = {}
		cls._cached_tilesets[tileset_name]['image'] = tileset_image
		cls._cached_tilesets[tileset_name]['config'] = tileset_config

	def create_tile(self, tile_value, *args, **kwargs):
		"""Creates a tile object from a numeric tile value.

		The arguments for the tile object should be passed when
		calling this method.

		Args:
			tile_value (int): The integer value of a tile in the tileset.

		Returns:
			The appropriate :class:`game.tiles.Tile` object for the tile value.
		"""
		# Merge the keyword arguments with any additional arguments from the tileset config
		kwargs = dict(kwargs.items() + self.config.get_tile_entry(tile_value).items())

		return tile_factory.create_tile(img=self.image.get_tile_image(tile_value), *args, **kwargs)

	@classmethod
	def load(cls, tileset_name, rows=None, cols=None):
		"""Loads a tileset.

		Args:
			tileset_name (str): The name of the tileset to load.

		Kwargs:
			rows (int): The number of rows of tiles in the tileset image.
			cols (int): The number of columns of tiles in the tileset image.

		Returns:
			A :class:`game.tiles.tileset.Tileset` object.
		"""
		# If this tileset's resources have not been loaded before, load and cache them
		if not tileset_name in cls._cached_tilesets:
			cls._cache_tileset(
				tileset_name,
				TilesetImage(get_tileset_image(tileset_name), rows, cols),
				TilesetConfig(get_tileset_config(tileset_name))
			)

		return cls(tileset_name, cls._cached_tilesets[tileset_name]['image'], cls._cached_tilesets[tileset_name]['config'])
