import pyglet
from pyglet.window import key
from ..settings import general_settings
from .. import util
import physicalobject

class Player(physicalobject.PhysicalObject):

	def __init__(self, key_handler, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)

		self.enabled = True

		self.hitbox.rel_x = general_settings.TILE_SIZE / 2
		self.hitbox.set_dimensions(general_settings.TILE_SIZE, general_settings.TILE_SIZE * 2)
		super(Player, self).update_positioning()

		self.max_dash_time = 0.5
		self.time_dashed = 0
		self.replenish_dash = False
		self.replenish_wait = 1

		self.max_walk_speed = 2 * general_settings.FPS # Max x velocity when walking
		self.max_dash_speed = 3 * self.max_walk_speed # Max x velocity when dashing
		self.max_speed = self.max_walk_speed

		self.walk_acceleration = 0.75
		self.dash_acceleration = 0.1
		self.acceleration_x = self.walk_acceleration

		self.key_handler = key_handler

	def disable(self):
		self.enabled = False
		self.target_speed = 0

	def enable(self):
		self.enabled = True

	def update(self, dt):
		# @TODO Better movement handling

		# @TODO There needs to be a dash meter overlay with 50px per 1 second of dash

		# Handle keyboard input

		if self.enabled:
			if self.key_handler[key.UP]:
				if not self.in_air:
					super(Player, self).jump();

			self.max_speed = self.max_walk_speed

			# Replenish the player's dash meter
			if self.replenish_dash:
				self.time_dashed -= dt

				if self.time_dashed <= 0:
					self.replenish_dash = False

			# Left shift is dashing
			if self.key_handler[key.LSHIFT] and not self.in_air and self.time_dashed < self.max_dash_time:
				# Cancel replenishing our dash now that we're using it
				self.replenish_dash = False
				pyglet.clock.unschedule(self.begin_replenishing_dash)

				# Begin dashing
				self.acceleration_x = self.dash_acceleration
				self.max_speed = self.max_dash_speed

				# Log our dash time
				self.time_dashed += dt

				# Begin replenishing dash after a short time
				pyglet.clock.schedule_once(self.begin_replenishing_dash, self.replenish_wait)
			elif not self.in_air:
				if abs(self.velocity_x) <= self.max_walk_speed:
					self.acceleration_x = self.walk_acceleration

			if self.key_handler[key.RIGHT]:
				self.target_speed = self.max_speed
			elif self.key_handler[key.LEFT]:
				self.target_speed = -self.max_speed
			else:
				self.target_speed = 0

			# Update our position
			super(Player, self).update(dt)

	# Begins replenishing the player's dash meter
	def begin_replenishing_dash(self, dt):
		self.replenish_dash = True
