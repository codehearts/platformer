from game.scripts import get_property_from_string
from . import install_translator

# Add support for translating level config strings to property values
install_translator('property', get_property_from_string)
