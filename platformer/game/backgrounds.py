import pyglet
from game import overlay

class Backgrounds(object):
    
    def __init__(self, tile_data, camera):
        self.bg_batch = pyglet.graphics.Batch()
        self.fg_batch = pyglet.graphics.Batch()
        self.camera = camera
        
        # @TODO At some point in the future, all of these keys should be made optional
        self.bg = pyglet.sprite.Sprite(img=pyglet.resource.image(tile_data['background']), x=camera.x, y=camera.y, batch=self.bg_batch)
        
        self.overlay = overlay.Overlay(tile_data, self.fg_batch, self.camera)
        
        # @TODO 2 or 3 layers of parallax backgrounds
        # @TODO Non-collidable background midground layer
        
        # @TODO Is this necessary?
        self.update(0)
    
    def update(self, dt):
        self.bg.x = self.camera.x
        self.bg.y = self.camera.y
        
        self.overlay.update(dt)
    
    # Draw the background to the screen
    def draw_background(self):
        self.bg_batch.draw()
    
    # Draw the foreground to the screen
    def draw_foreground(self):
        self.fg_batch.draw()
        self.overlay.draw()