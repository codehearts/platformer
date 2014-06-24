from game.tiles import Tileset
from . import install_translator

install_translator('tileset', Tileset.load)
