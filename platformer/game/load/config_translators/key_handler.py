from game import key_handler
from . import install_translator

# Add support for obtaining the key handler in level config files
install_translator('key_handler', lambda x: key_handler)
