import pyglet, math, transition
from settings import general_settings

class Overlay(object):
    
    def __init__(self, tile_data, batch, camera):
        self.show_fps = True
        
        self.batch = batch
        self.camera = camera
        
        self.tile_width = int(math.ceil(camera.width / general_settings.TILE_SIZE_FLOAT))
        self.tile_height = int(math.ceil(camera.height / general_settings.TILE_SIZE_FLOAT))
        
        self.transition = transition.Transition(self.camera, tile_data['name'])
        
        if self.show_fps:
            self.fps_text = pyglet.text.Label(str(pyglet.clock.get_fps()), font_name='Helvetica Neue', font_size=18, x=self.camera.x+10, y=self.camera.y2-10, batch=self.batch)
    
    def update(self, dt):
        if self.show_fps:
            self.fps_text.text = str(int(pyglet.clock.get_fps()))
            self.fps_text.x = self.camera.x + 10
            self.fps_text.y = self.camera.y + 10
        
        if self.transition:
            self.transition.update(dt)
    
    
    def draw(self):
        if self.transition:
            self.transition.draw()
            
            if self.transition.is_done:
                self.transition = None