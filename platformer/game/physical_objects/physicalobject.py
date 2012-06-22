import pyglet, math
from game import util
#from game import profilehooks
from ..settings import general_settings

class PhysicalObject(pyglet.sprite.Sprite):
    
    def __init__(self, stage, mass=1, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        
        self.x = int(self.x)
        self.y = int(self.y)
        
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height
        self.half_width = int(self.width/2)
        self.half_height = int(self.height/2)
        
        self.tile_width = self.width / general_settings.TILE_SIZE_FLOAT
        self.tile_height = self.height / general_settings.TILE_SIZE_FLOAT
        
        self.tile_x = self.x / general_settings.TILE_SIZE
        self.tile_y = self.y / general_settings.TILE_SIZE
        self.sub_tile_x = self.x % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
        self.sub_tile_y = self.y % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
        
        # @TODO It may be faster to keep a bytearray of this to check for collisions against
        self.stage = stage
        self.max_stage_x = len(self.stage[0])
        self.max_stage_y = len(self.stage)
        
        self.x_tile_span = self.get_x_tile_span()
        self.y_tile_span = self.get_y_tile_span()
        
        self.target_speed = 0
        
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = util.get_gravitational_acceleration(mass)
        #self.max_velocity_y # @TODO I should probably implement these
        #self.max_velocity_x
        
        self.facing_right = True
        self.in_air = True
        self.is_jumping = False    
    
    
    
    def move_to(self, new_x, new_y):
        # Handle horizontal component first in case of slopes
        if new_x != self.x:
            self.move_to_x(new_x)
        
        self.move_to_y(new_y)
    
    
    
    # Returns the tiles covered by single-dimensional movement on the specified axis
    def get_axis_range(self, axis, new_position):
        # Initiate our values based on the axis we're checking
        if axis == 'x':
            current_position = self.x
            current_tile = self.tile_x
            axis_dimension = self.tile_width
            axis_tile_boundary = self.max_stage_x - 1
        else: # Y axis
            current_position = self.y
            current_tile = self.tile_y
            axis_dimension = self.tile_height
            axis_tile_boundary = self.max_stage_y - 1
        
        new_tile = new_position / general_settings.TILE_SIZE
        
        # Ensure that we include the most tiles possible in the calculated range
        if new_position > current_position:
            new_tile = int(new_tile + axis_dimension) # Value is floored
            current_tile =  int(current_tile + axis_dimension)
            
            # Only check within the bounds of the stage
            if current_tile < 0:
                current_tile = 0
            
            if new_tile >= axis_tile_boundary:
                new_tile = axis_tile_boundary
            
            return xrange(current_tile, new_tile + 1)
        else:
            new_tile = int(new_tile) # Value is floored
            
            # Only check within the bounds of the stage
            if current_tile >= axis_tile_boundary:
                current_tile = axis_tile_boundary
            
            if new_tile < 0:
                new_tile = 0
            
            # Optimize for left-to-right or top-to-bottom checking
            return xrange(current_tile, new_tile - 1, -1)
    
    def move_to_x(self, new_x):
        x_range = self.get_axis_range('x', new_x)
        
        tile_found = False
        for y in self.y_tile_span:
            if tile_found:
                break
            
            for x in x_range:
                collision_tile = self.stage[y][x]
                if collision_tile:
                    
                    if collision_tile.is_slope():
                        # Allow the object to overlap slopes from their sloped side, but not their taller side
                        if (not collision_tile.is_collidable()) or (collision_tile.is_right_slope() and collision_tile.x2 > self.x) or (collision_tile.is_left_slope() and self.x2 > collision_tile.x):
                            continue
                    
                    if new_x < self.x: # Moving left
                        # If we're on a slope, ignore adjacent tiles to prevent getting stuck when ascending a leftward ramp
                        possible_slope = self.stage[y][x+1]
                        if possible_slope and possible_slope.is_left_slope():
                            continue
                        
                        new_x = collision_tile.x2
                        self.on_left_collision(collision_tile)
                    else: # Moving right
                        # If we're on a slope, ignore adjacent tiles to prevent getting stuck when ascending a rightward ramp
                        possible_slope = self.stage[y][x-1]
                        if possible_slope and possible_slope.is_right_slope():
                            continue
                        
                        new_x = collision_tile.x - self.width
                        self.on_right_collision(collision_tile)
                    
                    tile_found = True
                    break
        
        new_x = int(new_x)
        
        if new_x != self.x:
            self.facing_right = new_x > self.x
        
        self.x = new_x
        self.x2 = self.x + self.width
        self.tile_x = self.x / general_settings.TILE_SIZE
        self.sub_tile_x = self.x % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
        self.x_tile_span = self.get_x_tile_span()
    
    #@profilehooks.profile
    def move_to_y(self, new_y):
        y_range = self.get_axis_range('y', new_y)
        
        tile_found = False
        for y in y_range:
            if tile_found:
                break
            
            for x in self.x_tile_span:
                collision_tile = self.stage[y][x]
                if collision_tile:
                    
                    if collision_tile.is_slope():
                        if new_y < self.y or collision_tile.is_upper_slope(): # Moving down
                            new_y = self.resolve_slope_collision(new_y, collision_tile, x, y)
                        elif self.y2 - collision_tile.y < 5:
                            # Collide with the bottoms of slope tiles
                            # A threshold of 5 pixels ensures that we don't collide with other tiles on a multi-tile slope when jumping
                            new_y = collision_tile.y - self.height
                            self.on_top_collision(collision_tile) 
                        
                        tile_found = True
                        break
                    
                    if new_y < self.y: # Moving down
                        # If there's a leftward slope tile to our right, we should be on that slope instead of this tile
                        possible_slope = self.stage[y][x+1]
                        if possible_slope and possible_slope.is_left_slope():
                            # Allows us to begin descending leftward slopes
                            new_y = self.resolve_slope_collision(new_y, self.stage[y][x+1], x+1, y)
                            tile_found = True
                            break
                        
                        new_y = collision_tile.y2
                        self.on_bottom_collision(collision_tile)
                    else: # Moving up
                        new_y = collision_tile.y - self.height
                        self.on_top_collision(collision_tile)
                    
                    tile_found = True
                    break
        
        # Handle falling
        if not (tile_found or self.in_air):
            self.in_air = True
        
        self.y = int(new_y)
        self.y2 = self.y + self.height
        self.tile_y = self.y / general_settings.TILE_SIZE
        self.sub_tile_y = self.y % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
        self.y_tile_span = self.get_y_tile_span()
    
    
    # @TODO Test ceiling slopes, I think they might be glitchy
    def resolve_slope_collision(self, new_y, slope_tile, x, y):
        # Position on the tile, from the center of this object (0 is left, 1 is right)
        position_on_tile = (self.x + self.half_width - slope_tile.x) / general_settings.TILE_SIZE_FLOAT
        
        change_tiles = False
        
        if position_on_tile < 0:
            # Allows us to descend rightward slopes
            possible_slope = self.stage[y-1][x-1]
            if possible_slope and possible_slope.is_right_slope():
                change_tiles = True
        elif position_on_tile > 1:
            # Allows us to ascend multi-tile rightward slopes and descend multi-tile leftward slopes
            possible_slope = self.stage[y][x+1]
            if possible_slope and slope_tile.get_slope_parts() == possible_slope.get_slope_parts():
                change_tiles = True
            else:
                # Allows us to descend leftward slopes
                possible_slope = self.stage[y-1][x+1]
                if possible_slope and possible_slope.is_left_slope():
                    change_tiles = True
                else:
                    # Prevents glitches around saw-like leftward slopes
                    possible_slope = self.stage[y][x+1]
                    if possible_slope and possible_slope.is_slope():
                        angle_change = slope_tile.is_left_slope() != possible_slope.is_left_slope()
                        
                        # If we're currently on a collidable rightward slope and our x-position overlaps it, ignore the tile to our right
                        usable_slope = not (slope_tile.is_collidable() and slope_tile.is_right_slope() and slope_tile.x2 >= self.x)
                        # If there's a collidable leftward slope to our right and our x-position doesn't overlap it, ignore it
                        usable_slope = usable_slope and not (possible_slope.is_collidable() and possible_slope.is_left_slope() and self.x2 <= possible_slope.x)
                        
                        if angle_change or usable_slope:
                            change_tiles = True
                    elif possible_slope:
                        # If it's not a slope, it's a wall tile
                        if not possible_slope.is_slope():
                            self.on_bottom_collision()
                            return possible_slope.y2
        else:
            # Check if we're overlaping the tall end of a leftward slope with our right side
            possible_slope = self.stage[y][x+1]
            if slope_tile.is_left_slope() and possible_slope and not possible_slope.is_right_slope() and slope_tile.get_slope_parts() != possible_slope.get_slope_parts() and self.x2 > possible_slope.x:
                # If it's not a slope, it's a wall tile
                if not possible_slope.is_slope():
                    self.on_bottom_collision()
                    return possible_slope.y2
                
                change_tiles = True
        
        if change_tiles:
            slope_tile = possible_slope
            position_on_tile = (self.x + self.half_width - slope_tile.x) / general_settings.TILE_SIZE_FLOAT
        
        if position_on_tile < 0:
            slope_y = slope_tile.get_slope_left_y()
        elif position_on_tile > 1:
            slope_y = slope_tile.get_slope_right_y()
        else:
            slope_y = int(math.ceil((1-position_on_tile)*slope_tile.get_slope_left_y() + position_on_tile*slope_tile.get_slope_right_y()))
        
        # If we've moved down onto another tile and we're not already in the air...
        if self.y >= slope_tile.y2 and not self.in_air:
            # Calculate a threshold based on how high our horizontal velocity could possible send us off a slope when descending it
            # If we're higher than this value, we're in the air
            # Assume 1/2 of the frame rate to be safe
            height_threshold = self.y - math.ceil(abs(self.velocity_x) / (slope_tile.get_slope_parts()*(pyglet.clock.get_fps()/2)))
            
            if height_threshold > slope_y:
                self.in_air = True
        
        # If we're on the ground or we're colliding with the slope, register the collision
        if (not self.in_air) or (new_y <= slope_y and not slope_tile.is_upper_slope()):
            new_y = slope_y
            self.on_bottom_collision()
        elif slope_tile.is_upper_slope() and new_y >= slope_y:
            new_y = slope_y - self.height
            self.on_top_collision()
        
        return new_y
    
    
    
    def on_right_collision(self, collision_tile=None):
        self.velocity_x = 0
    
    def on_left_collision(self, collision_tile=None):
        self.velocity_x = 0
    
    def on_bottom_collision(self, collision_tile=None):
        self.velocity_y = 0
        
        # Handle landing from a jump or fall
        if self.in_air:
            self.on_land()
    
    def on_top_collision(self, collision_tile=None):
        self.velocity_y = 0
    
    def on_land(self):
        self.in_air = False
        self.is_jumping = False
        self.is_falling = False
    
    
    
    def get_x_tile_span(self):
        min_x = self.tile_x
        if min_x < 0:
            min_x = 0
        max_x = int(math.ceil(self.tile_x + self.sub_tile_x + self.tile_width))
        if max_x > self.max_stage_x:
            max_x = self.max_stage_x
        
        return range(min_x, max_x)
    
    def get_y_tile_span(self):
        min_y = self.tile_y
        if min_y < 0:
            min_y = 0
        max_y = int(math.ceil(self.tile_y + self.sub_tile_y + self.tile_height))
        if max_y > self.max_stage_y:
            max_y = self.max_stage_y
        
        return range(min_y, max_y)
    
    
    
    def get_coordinates(self):
        return (self.x, self.y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_dimensions(self):
        return (int(self.width), int(self.height))
    
    def get_width(self):
        return int(self.width)
    
    def get_half_width(self):
        return int(self.half_width)
    
    def get_half_height(self):
        return int(self.half_height)
    
    def get_height(self):
        return int(self.height)
    
    def get_velocity(self):
        return (self.velocity_x, self.velocity_y)
    
    def get_acceleration(self):
        return (self.acceleration_x, self.acceleration_y)
    
    
    
    def reset_to(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height
        
        self.tile_x = self.x / general_settings.TILE_SIZE
        self.tile_y = self.y / general_settings.TILE_SIZE
        self.sub_tile_x = self.x % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
        self.sub_tile_y = self.y % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
        
        self.x_tile_span = self.get_x_tile_span()
        self.y_tile_span = self.get_y_tile_span()
        
        self.set_velocity(0, 0)
        self.in_air = True
    
    def reset_to_tile(self, tile_x, tile_y):
        self.reset_to(tile_x * general_settings.TILE_SIZE, tile_y * general_settings.TILE_SIZE)
    
    def set_velocity(self, vx, vy):
        self.velocity_x = vx
        self.velocity_y = vy
    
    def set_acceleration(self, ax, ay):
        self.acceleration_x = ax
        self.acceleration_y = ay
    
    
    
    def jump(self):
        """For when this object jumps off solid ground"""
        self.in_air = True
        self.is_jumping = True
        
        # @TODO This should be an "accelerated" jump based on keyboard input
        # @TODO Other physical objects should be able to vary their jump acceleration as well, hence putting the code here
        self.velocity_y = -self.acceleration_y / 2 # @TODO Figure out how to get a good value for this
    
    
    
    def detect_collisions(self):
        # @TODO This method needs to check for collisions with the player (only npcs should use this)
        # @TODO Or would it be better to have the player check for other collisions? NO, because he updates before the characters
        """if util.collision_detected(collision_tile, self):
            self.handle_collision_with(collision_tile)
            collision_tile.handle_collision_with(self)"""
    
    def handle_collision_with(self, other_obj):
        # @TODO Handle collisions with other characters
        pass
    
    
    
    def update(self, dt):
        # Limit horizontal acceleration when in air
        if self.in_air:
            aerial_acceleration = self.acceleration_x * 0.2
            self.velocity_x = (aerial_acceleration*self.target_speed + (1-aerial_acceleration)*self.velocity_x)
        else:
            self.velocity_x = (self.acceleration_x*self.target_speed + (1-self.acceleration_x)*self.velocity_x)
        
        if abs(self.velocity_x) <= abs(self.target_speed) + 1:
            self.velocity_x = self.target_speed
        
        self.velocity_y += self.acceleration_y * dt
        
        self.move_to(self.x + self.velocity_x * dt, self.y + self.velocity_y * dt)