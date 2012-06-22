import pyglet, animation
from ..settings import general_settings

# Transition spritesheet

image = pyglet.resource.image('transition.png')
sheet = pyglet.image.ImageGrid(image, 1, 31)
#sheet = pyglet.image.TextureGrid(pyglet.image.ImageGrid(image, 1, 31))



# Transition sprite

sprite = []
for i in xrange(0, 31):
    sprite.append(pyglet.image.TileableTexture.create_for_image(sheet[i]))
#sprite = animation.make_from(sheet, range(0, 31), [general_settings.FRAME_LENGTH])