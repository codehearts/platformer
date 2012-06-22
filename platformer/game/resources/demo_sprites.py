import pyglet

# Demo character sprites

image = pyglet.resource.image('test_aura_1.png')
frames = pyglet.image.TextureGrid(pyglet.image.ImageGrid(image, 1, 10))

# Floating sprite

# @TODO Honestly we need a class to handle setting this stuff up
floating_frame_time = 0.1
floating = pyglet.image.Animation([
    pyglet.image.AnimationFrame(frames[0], floating_frame_time),
    pyglet.image.AnimationFrame(frames[1], floating_frame_time),
    pyglet.image.AnimationFrame(frames[2], floating_frame_time),
    pyglet.image.AnimationFrame(frames[3], floating_frame_time),
    pyglet.image.AnimationFrame(frames[4], floating_frame_time),
    pyglet.image.AnimationFrame(frames[5], floating_frame_time),
    pyglet.image.AnimationFrame(frames[6], floating_frame_time),
    pyglet.image.AnimationFrame(frames[7], floating_frame_time),
    pyglet.image.AnimationFrame(frames[8], floating_frame_time),
    pyglet.image.AnimationFrame(frames[9], floating_frame_time)
])