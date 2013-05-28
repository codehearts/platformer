#import pyglet, animation
import pyglet
#from ..settings import general_settings

# Transition spritesheet
# TODO This sort of thing should be defined dynamically

image = pyglet.resource.image('transition.png')
sheet = pyglet.image.ImageGrid(image, 1, 31)
#sheet = pyglet.image.TextureGrid(pyglet.image.ImageGrid(image, 1, 31))



# Transition sprite

sprite = [pyglet.image.TileableTexture.create_for_image(still_frame) for still_frame in sheet]
#sprite = animation.make_from(sheet, range(0, 31), [general_settings.FRAME_LENGTH])
