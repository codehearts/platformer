import pyglet
from pyglet.window import key
from game.graphics import install_graphics_module
from ..settings import general_settings
from hitbox_physical_object import HitboxPhysicalObject
import game.load

class Player(HitboxPhysicalObject):

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(*args, **kwargs)

		self.enabled = True

		self.hitbox_offset_x = general_settings.TILE_SIZE / 2
		self.hitbox.width = general_settings.TILE_SIZE
		self.hitbox.height = general_settings.TILE_SIZE * 2

		self.max_dash_time = 0.5
		self.time_dashed = 0
		self.replenish_dash = False
		self.replenish_wait = 1

		self.max_walk_speed = 250 # Max x velocity when walking
		self.max_dash_speed = 3 * self.max_walk_speed # Max x velocity when dashing
		self.max_speed = self.max_walk_speed

		self.walk_acceleration = 0.75
		self.dash_acceleration = 0.1
		self.acceleration_x = self.walk_acceleration

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



def recognizer(graphics_type):
	"""Recognizes whether this graphics type is handled by :class:`game.physical_objects.Player`."""
	return graphics_type == 'player'

def factory(*args, **kwargs):
	"""Returns a :class:`game.physical_objects.Player` for the given arguments."""
	return game.load.Player(*args, **kwargs)

install_graphics_module(__name__)
