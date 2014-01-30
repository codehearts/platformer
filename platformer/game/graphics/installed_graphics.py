from sys import modules

installed_graphics = []
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
