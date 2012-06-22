import pyglet, easing
from pyglet.gl import *
from resources import transition_sprite

class Transition(object):
    
    def __init__(self, camera, title=''):
        self.title = title
        self.camera = camera
        
        self.is_done = False
        
        self.frame_count = len(transition_sprite.sprite)
        self.current_frame = 0
        self.first_frame_time = 0.5
        self.total_frame_time = 1.25
        self.frame_time_progress = 0
        
        self.title = pyglet.text.Label(title, font_name='Helvetica Neue', font_size=18, anchor_x='center', anchor_y='center')
        
        self.total_title_time = 2.25
        self.title_time_progress = 0
    
    def update(self, dt):
        self.frame_time_progress += dt
        self.title_time_progress += dt
        
        self.title.x = self.camera.focus_x
        self.title.y = self.camera.focus_y
    
    def draw(self):
        if self.current_frame < self.frame_count:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            transition_sprite.sprite[self.current_frame].blit_tiled(self.camera.x, self.camera.y, 1, self.camera.width, self.camera.height)
            
            # Update the frame on an easing function if we're past the first frame
            if self.frame_time_progress > self.first_frame_time:
                self.advance_frame()
        
        if self.title_time_progress <= self.total_title_time:
            self.title.draw()
        else:
            self.is_done = True
    
    def advance_frame(self):
        self.current_frame = int(easing.ease_out(1, self.frame_count, self.total_frame_time, self.frame_time_progress-self.first_frame_time, 1.75))