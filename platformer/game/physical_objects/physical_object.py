import pyglet, math
from game import util
#from game import profilehooks
from ..settings import general_settings
from collision_resolver import resolve_collisions

# TODO Create a HitboxPhysicalObject class and a MultiHitboxPhysicalObject class

# TODO This implementation of PhysicalObject should replace the other one
class PhysicalObject(pyglet.sprite.Sprite):

	# TODO Shouldn't these new kwargs be handled by calling pop on kwargs before calling super?
	def __init__(self, stage, mass=1, key_handler=None, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)

		self.hitbox = util.HitBox(self.x, self.y, 0, 0, self.width, self.height)

		# @TODO It may be faster to keep a bytearray of this to check for collisions against
		self.stage = stage
		self.max_stage_x = len(self.stage[0])
		self.max_stage_y = len(self.stage)

		# Update our positioning based on our hitbox
		self.update_positioning()

		self.target_speed = 0

		self.velocity_x = 0.0
		self.velocity_y = 0.0
		self.acceleration_x = 1.0 # Instantaneous acceleration
		self.acceleration_y = util.get_gravitational_acceleration(mass)
		#self.max_velocity_y # @TODO I should probably implement these
		#self.max_velocity_x

		# Where this object is attempting to move to when being updated
		self.moving_to_x = None
		self.moving_to_y = None

		self.facing_right = True
		self.in_air = True
		self.is_jumping = False

		self.key_handler = key_handler



	# TODO This method could be removed
	def move_to(self, new_x, new_y):
		resolve_collisions(self)

	# Updates the sprite's positioning relative to the hitbox
	def update_positioning(self):
		self.x = int(self.hitbox.x - self.hitbox.rel_x)
		self.y = int(self.hitbox.y - self.hitbox.rel_y)

		self.tile_width = self.hitbox.width / general_settings.TILE_SIZE_FLOAT
		self.tile_height = self.hitbox.height / general_settings.TILE_SIZE_FLOAT

		self.tile_x = self.hitbox.x / general_settings.TILE_SIZE
		self.tile_y = self.hitbox.y / general_settings.TILE_SIZE
		self.sub_tile_x = self.hitbox.x % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
		self.sub_tile_y = self.hitbox.y % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT

		self.x_tile_span = self.get_x_tile_span()
		self.y_tile_span = self.get_y_tile_span()


	def on_right_collision(self, collision_tile=None):
		self.target_speed = 0
		self.velocity_x = 0

	def on_left_collision(self, collision_tile=None):
		self.target_speed = 0
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



	# TODO Remove these in favor of Pythonic attribute getters and setters
	def get_coordinates(self):
		return (self.hitbox.x, self.hitbox.y)

	def get_x(self):
		return self.hitbox.x

	def get_y(self):
		return self.hitbox.y

	def get_dimensions(self):
		return (self.hitbox.width, self.hitbox.height)

	def get_width(self):
		return self.hitbox.width

	def get_height(self):
		return self.hitbox.height

	def get_half_width(self):
		return self.hitbox.half_width

	def get_half_height(self):
		return self.hitbox.half_height

	def get_velocity(self):
		return (self.velocity_x, self.velocity_y)

	def get_acceleration(self):
		return (self.acceleration_x, self.acceleration_y)



	def reset_to(self, new_x, new_y):
		self.set_x(new_x)
		self.set_y(new_y)

		self.set_velocity(0, 0)
		self.in_air = True

	def reset_to_tile(self, tile_x, tile_y):
		self.reset_to(tile_x * general_settings.TILE_SIZE, tile_y * general_settings.TILE_SIZE)

	def set_x(self, new_x):
		self.hitbox.set_x(new_x)
		self.x = self.hitbox.x - self.hitbox.rel_x
		self.tile_x = self.hitbox.x / general_settings.TILE_SIZE
		self.sub_tile_x = self.hitbox.x % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
		self.x_tile_span = self.get_x_tile_span()

	def set_y(self, new_y):
		self.hitbox.set_y(new_y)
		self.y = self.hitbox.y - self.hitbox.rel_y
		self.tile_y = self.hitbox.y / general_settings.TILE_SIZE
		self.sub_tile_y = self.hitbox.y % general_settings.TILE_SIZE / general_settings.TILE_SIZE_FLOAT
		self.y_tile_span = self.get_y_tile_span()

	def set_velocity(self, vx, vy):
		self.velocity_x = vx
		self.target_speed = vx
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

		self.moving_to_x = self.hitbox.x + self.velocity_x * dt
		self.moving_to_y = self.hitbox.y + self.velocity_y * dt
		self.move_to(self.moving_to_x, self.moving_to_y)
