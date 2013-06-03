from pyglet.resource import file as open_file
from pyglet.resource import image as open_image
from pyglet.resource import ResourceNotFoundException
from ...settings.general_settings import TILESET_DIRECTORY

def load_tileset_file(tileset_name, name):
	"""Loads a tileset resource file.

	Args:
		tileset_name (str): The name of the tileset to load a resource from.
		name (str): Filename of the resource load.

	Returns:
		A file object for the loaded resource.

	Raises:
		ResourceNotFoundException: The resource to load could not be found.
	"""
	return open_file(TILESET_DIRECTORY+'/'+tileset_name+'/'+name)

def load_tileset_image(tileset_name, name):
	"""Loads a tileset image file.

	Args:
		tileset_name (str): The name of the tileset to load an image from.
		name (str): Filename of the image source to load.

	Returns:
		A :class:`pyglet.image.Texture` object of the image.

	Raises:
		ResourceNotFoundException: The resource to load could not be found.
	"""
	return open_image(TILESET_DIRECTORY+'/'+tileset_name+'/'+name)

# TODO Unit tests
def get_tileset_config(tileset_name):
	"""Loads the contents of the config file for a tileset.

	If the config file can not be opened, an empty string is returned.

	Args:
		tileset_name (str): The name of the tileset to load the config for.

	Returns:
		The contents of the config file as a string. If the file could not
		be openned, its "contents" are assumed to be an empty string.
	"""
	try:
		return load_tileset_file(tileset_name, 'config.json').read()
	except ResourceNotFoundException:
		return ''

# TODO Unit tests
def get_tileset_image(tileset_name):
	"""Loads the image file for a tileset.

	Because tileset images can be one of multiple image formats,
	this loader searches for gif, then png, then jpg, then jpeg.
	If a tile image can not be found for any of those formats, an
	exception is raised.

	Args:
		tileset_name (str): The name of the tileset to load the image for.

	Returns:
		A :class:`pyglet.image.Texture` object of the image.

	Raises:
		ResourceNotFoundException: The resource to load could not be found.
	"""
	# Try opening a "tiles.*" file in this order
	filetypes = ['gif', 'png', 'jpg', 'jpeg']

	for filetype in filetypes:
		try:
			return load_tileset_image(tileset_name, 'tiles.'+filetype)
		except ResourceNotFoundException:
			# If we've checked all of the filetypes, it doesn't exist
			if filetype is filetypes[-1]:
				raise ResourceNotFoundException()
