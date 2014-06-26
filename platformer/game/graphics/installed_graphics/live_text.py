from game.text import LiveText
from . import install_graphics_module

def recognizer(graphics_type):
        """Recognizes whether this graphics type is handled by :class:`game.text.live_text.LiveText`."""
        return graphics_type == 'live text'

def factory(*args, **kwargs):
        """Returns a :class:`game.text.live_text.LiveText` for the given arguments."""
        return LiveText(kwargs.pop('text_source'), *args, **kwargs)

install_graphics_module(__name__)
