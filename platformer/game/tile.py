import pyglet.sprite
from settings import general_settings, tile_settings

class Tile(pyglet.sprite.Sprite):
    
    def __init__(self, tile_type=0, *args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)
        
        self.x = int(self.x)
        self.y = int(self.y)
        self.x2 = self.x + int(self.width)
        self.y2 = self.y + int(self.height)
        
        self.tile_x = self.x / general_settings.TILE_SIZE
        self.tile_y = self.y / general_settings.TILE_SIZE
        
        self.type = tile_type
        self.type_is_left_slope = False
        self.type_is_right_slope = False
        self.type_is_upper_slope = False
        self.slope_parts = 0
        
        self.collidable = True
        
        if self.type == tile_settings.RIGHT_SLOPE_1:
            self.slope_parts = 1.0
            self.type_is_right_slope = True
            self.slope_right_y = self.y + tile_settings.RIGHT_SLOPE_1_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.RIGHT_SLOPE_1_LEFT_Y
        elif self.type == tile_settings.LEFT_SLOPE_1:
            self.slope_parts = 1.0
            self.type_is_left_slope = True
            self.slope_right_y = self.y + tile_settings.LEFT_SLOPE_1_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.LEFT_SLOPE_1_LEFT_Y
        elif self.type == tile_settings.TOP_LEFT_SLOPE_1:
            self.slope_parts = 1.0
            self.type_is_left_slope = True
            self.type_is_upper_slope = True
            self.slope_right_y = self.y + tile_settings.TOP_LEFT_SLOPE_1_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.TOP_LEFT_SLOPE_1_LEFT_Y
        elif self.type == tile_settings.RIGHT_SLOPE_2_1:
            self.slope_parts = 2.0
            self.collidable = False
            self.type_is_right_slope = True
            self.slope_right_y = self.y + tile_settings.RIGHT_SLOPE_2_1_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.RIGHT_SLOPE_2_1_LEFT_Y
        elif self.type == tile_settings.RIGHT_SLOPE_2_2:
            self.slope_parts = 2.0
            self.type_is_right_slope = True
            self.slope_right_y = self.y + tile_settings.RIGHT_SLOPE_2_2_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.RIGHT_SLOPE_2_2_LEFT_Y
        elif self.type == tile_settings.LEFT_SLOPE_2_1:
            self.slope_parts = 2.0
            self.type_is_left_slope = True
            self.slope_right_y = self.y + tile_settings.LEFT_SLOPE_2_1_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.LEFT_SLOPE_2_1_LEFT_Y
        elif self.type == tile_settings.LEFT_SLOPE_2_2:
            self.slope_parts = 2.0
            self.collidable = False
            self.type_is_left_slope = True
            self.slope_right_y = self.y + tile_settings.LEFT_SLOPE_2_2_RIGHT_Y
            self.slope_left_y = self.y + tile_settings.LEFT_SLOPE_2_2_LEFT_Y
        
        self.type_is_slope = self.type_is_left_slope or self.type_is_right_slope
    
    def is_collidable(self):
        return self.collidable
    
    def is_normal(self):
        return self.type == tile_settings.NORMAL
    
    def is_left_slope(self):
        return self.type_is_left_slope
    
    def is_right_slope(self):
        return self.type_is_right_slope
    
    def is_upper_slope(self):
        return self.type_is_upper_slope
    
    def is_slope(self):
        return self.type_is_slope
    
    def get_slope_right_y(self):
        return self.slope_right_y
    
    def get_slope_left_y(self):
        return self.slope_left_y
    
    def get_slope_parts(self):
        return self.slope_parts
    
    def update(self, dt):
        pass
    
    def handle_collision_with(self, other_obj):
        pass