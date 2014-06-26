from game.scripts import get_window_width, get_window_height
from . import install_translator

# Add support for translating level config strings to window dimensions
install_translator('window_width', get_window_width)
install_translator('window_height', get_window_height)
