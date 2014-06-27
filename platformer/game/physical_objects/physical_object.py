from game import util
from game.extended_sprite import ExtendedSprite
#from game import profilehooks
from ..settings import general_settings
from collision_resolver import resolve_collisions

# TODO This implementation of PhysicalObject should replace the other one
# TODO Test this class's coordinates!
class PhysicalObject(ExtendedSprite):

	def __init__(self, stage, *args, **kwargs):
		mass = kwargs.pop('mass', 1)
		key_handler = kwargs.pop('key_handler', None)
		super(PhysicalObject, self).__init__(*args, **kwargs)

		# @TODO It may be faster to keep a bytearray of this to check for collisions against
		self.stage = stage
		self.max_stage_x = len(self.stage[0])
		self.max_stage_y = len(self.stage)

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


	# TODO set_state(str) method, which sets the state of the object and can be used for changing the displayed object sprite


	def on_right_collision(self, collision_tile=None):
		self.target_speed = 0
		self.velocity_x = 0
		self.acceleration_x = 0

	def on_left_collision(self, collision_tile=None):
		self.target_speed = 0
		self.velocity_x = 0
		self.acceleration_x = 0

	def on_bottom_collision(self, collision_tile=None):
		self.velocity_y = 0

		# Handle landing from a jump or fall
		if self.in_air:
			self.on_land()

	def on_top_collision(self, collision_tile=None):
		self.velocity_y = 0

	# TODO Use a better, less ambiguous name for this
	def on_land(self):
		self.in_air = False
		self.is_jumping = False
		self.is_falling = False



	def get_x_tile_span(self):
		return range(max(0, self.x_tile), min(self.max_stage_x, self.x2_tile + 1))
		#min_x = self.tile_x
		#if min_x < 0:
			#min_x = 0
		#max_x = int(math.ceil(self.tile_x + self.sub_tile_x + self.tile_width))
		#if max_x > self.max_stage_x:
			#max_x = self.max_stage_x

		#return range(min_x, max_x)

	def get_y_tile_span(self):
		return range(max(0, self.y_tile), min(self.max_stage_y, self.y2_tile + 1))
		#min_y = self.tile_y
		#if min_y < 0:
			#min_y = 0
		#max_y = int(math.ceil(self.tile_y + self.sub_tile_y + self.tile_height))
		#if max_y > self.max_stage_y:
			#max_y = self.max_stage_y

		#return range(min_y, max_y)



	# TODO Remove these in favor of Pythonic attribute getters and setters
	def get_coordinates(self):
		return (self.x, self.y)

	def get_dimensions(self):
		return (self.width, self.height)

	def get_velocities(self):
		return (self.velocity_x, self.velocity_y)

	def get_accelerations(self):
		return (self.acceleration_x, self.acceleration_y)



	def reset_to(self, new_x, new_y):
		self.x = new_x
		self.y = new_y

		self.velocity_x, self.velocity_y = (0, 0)
		self.in_air = True

	def reset_to_tile(self, tile_x, tile_y):
		self.reset_to(tile_x * general_settings.TILE_SIZE, tile_y * general_settings.TILE_SIZE)

	def set_velocities(self, vx, vy):
		# TODO Pythonic setter for velocity_x
		self.velocity_x = vx
		self.target_speed = vx
		self.velocity_y = vy

	def set_accelerations(self, ax, ay):
		self.acceleration_x = ax
		self.acceleration_y = ay



	def jump(self):
		"""For when this object jumps off solid ground"""
		self.in_air = True
		self.is_jumping = True

		# @TODO This should be an "accelerated" jump based on keyboard input
		# @TODO Other physical objects should be able to vary their jump acceleration as well, hence putting the code here
		self.velocity_y = -self.acceleration_y / 2 # @TODO Figure out how to get a good value for this, preferably one that determines how many tiles high they can jump



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

		self.moving_to_x = self.x + self.velocity_x * dt
		self.moving_to_y = self.y + self.velocity_y * dt
		self.move_to(self.moving_to_x, self.moving_to_y)
