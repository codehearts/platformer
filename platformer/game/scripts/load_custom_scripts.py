from ..settings.general_settings import RESOURCE_PATH, SCRIPT_DIRECTORY, SCRIPT_FORMAT
from imp import load_source
"""Python 3
import importlib.machinery"""

def load_custom_scripts(scripts):
	"""Dynamically loads custom scripts from the game's scripts resource directory.

	Args:
		scripts (list): A list of the filenames of the scripts to load.
	"""
	for script in scripts:
		load_source('game.scripts.custom.'+script, RESOURCE_PATH+SCRIPT_DIRECTORY+'/'+script+'.'+SCRIPT_FORMAT)
		"""Python 3
		loader = importlib.machinery.SourceFileLoader('games.scripts.custom.'+script, RESOURCE_PATH+SCRIPT_DIRECTORY+'/'+script+'.'+SCRIPT_FORMAT)
		loader.load_module('game.scripts.custom.'+script)"""
