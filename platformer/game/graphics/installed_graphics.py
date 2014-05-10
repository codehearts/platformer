from pyglet.resource import image as open_resource_image
from pyglet.sprite import Sprite
from sys import modules

def install_graphics_module(module_name):
    """Installs the specified module to be used for graphical output.

    Args:
        module_name (string): The name of the module to install.
    """
    global installed_graphics

    graphics_module = modules[module_name]
    installed_graphics.append({
        'recognizer': graphics_module.recognizer,
        'factory': graphics_module.factory,
    })



def _sprite_factory(*args, **kwargs):
    """Returns a :class:`pyglet.sprite.Sprite` for the given arguments."""
    return Sprite(img=open_resource_image(kwargs['graphic']), *args)

installed_graphics = [
    # Pre-install Pyglet's Sprite module
    {
        'recognizer': lambda graphics_type: graphics_type == 'image',
        'factory': _sprite_factory,
    }
]
