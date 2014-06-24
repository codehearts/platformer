from pyglet.window import key
import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

# Global level variable
level = None
# Handler for all keyboard events
key_handler = key.KeyStateHandler()
