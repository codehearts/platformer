from installed_graphics import installed_graphics

def create_graphics_object(graphics_type, *args, **kwargs):
    """Creates a graphics object of the specified type with the given arguments.

    In addition to this method's arguments, the graphic object's arguments should
    be passed as well.

    This factory will only return types that have been installed via the
    installed_graphics module.

    Installed graphics modules must provide a `recognizer` method which
    accepts a graphics type as a string and returns true if that string
    represents that graphics module and false otherwise.

    Installed graphics modules must also provide a `factory` method which
    creates an object of the appropriate graphics class from the given
    graphics arguments.

    Args:
        graphics_type (string): The graphics type to create.

    Returns:
        A graphics object from the appropriate class.
    """
    global installed_graphics
    for installed_graphic in installed_graphics:
        if installed_graphic['recognizer'](graphics_type):
            return installed_graphic['factory'](*args, **kwargs)

    raise ValueError('Could not create graphics object: invalid graphics type')
