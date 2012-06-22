import pyglet, animation

# Player sprites

image = pyglet.resource.image('dog.png')
sheet = pyglet.image.TextureGrid(pyglet.image.ImageGrid(image, 1, 2))



# Standing sprite

standing = animation.make_from(sheet, range(0, 2), [0.5])