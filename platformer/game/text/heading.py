from game.graphics import install_graphics_module
from text import Text

# TODO What's the point of this class? It functions almost exactly as text.Text
class Heading(Text):
    """A text label intended for headings.

    A Heading object can be created by the graphics
    factory by specifying "heading" as the graphics type.
    """

    def __init__(self, *args, **kwargs):
        # Set the default font size to 18
        if not 'font_size' in kwargs:
            kwargs['font_size'] = 18

        super(Heading, self).__init__(*args, **kwargs)



def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.text.heading.Heading`."""
	return graphics_type == 'heading'

def factory(*args, **kwargs):
	"""Returns a :class:`game.text.heading.Heading` for the given arguments."""
	return Heading(*args, **kwargs)

install_graphics_module(__name__)
