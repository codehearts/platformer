import physicalobject
from ..settings import general_settings

class SimpleAI(physicalobject.PhysicalObject):
    
    def __init__(self, speed=150, *args, **kwargs):
        super(SimpleAI, self).__init__(*args, **kwargs)
        
        self.speed = speed
        
        self.destination_x = None
    
    def go_to_x(self, new_x):
        new_x = int(new_x)
        
        self.destination_x = new_x
        if new_x < self.x: # Moving left
            self.velocity_x = -self.speed
        else: # Moving right
            self.velocity_x = self.speed
    
    def go_to_tile_x(self, new_tile_x):
        self.go_to_x(new_tile_x * general_settings.TILE_SIZE)
    
    def reset_to(self, x, y):
        super(SimpleAI, self).reset_to(x, y)
        
        self.destination_x = None
    
    
    
    def update(self, dt):
        super(SimpleAI, self).update(dt)
        
        if (self.velocity_x < 0 and self.x <= self.destination_x) or (self.velocity_x > 0 and self.x >= self.destination_x):
            self.x = self.destination_x
            self.destination_x = None
            self.velocity_x = 0