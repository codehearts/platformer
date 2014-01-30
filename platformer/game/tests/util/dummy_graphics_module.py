"""Provides a custom graphics module for testing with.

A ``DummyGraphics`` class is defined but not installed by this module.
This module also defines the necessary ``recognizer`` and ``factory``
functions, recognizing the string defined by the ``recognized_name``
property.
"""

recognized_name = 'testing dummy graphic'

class DummyGraphics(object):
    """Dummy class for testing graphics installation and instantiation.

    Attributes:
        name (string): The name of the dummy graphic.
        desc (string): A description of the dummy graphic.
    """

    def __init__(self, name, desc="No description"):
        """Creates a dummy graphics object.

        Args:
            name (string): The name of the dummy graphic.

        Kwargs:
            desc (string): A description of the dummy graphic.
        """
        self.name = name
        self.desc = desc

def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by the dummy class."""
	return graphics_type == recognized_name

def factory(*args, **kwargs):
	"""Returns a DummyGraphics object with the given arguments."""
	return DummyGraphics(*args, **kwargs)
