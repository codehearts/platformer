from game.load.installed_level_config_translators import install_level_config_translator

# TODO Obtain the window width from the actual window object
def get_window_width(property_value):
	"""Returns the width of the window."""
	return 800

# TODO Obtain the window height from the actual window object
def get_window_height(property_value):
	"""Returns the height of the window."""
	return 600

# Add support for translating level config strings to window dimensions
install_level_config_translator('window_width', get_window_width)
install_level_config_translator('window_height', get_window_width)
