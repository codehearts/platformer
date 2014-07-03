from hitbox_physical_object import HitboxPhysicalObject
from ..settings.general_settings import TILE_SIZE

class SimpleAI(HitboxPhysicalObject):

	def __init__(self, *args, **kwargs):
		self.speed = kwargs.pop('speed', 150)

		super(SimpleAI, self).__init__(*args, **kwargs)

		self.movement_acceleration = 1

		self.destination_x = None

	def go_to_x(self, new_x):
		new_x = int(new_x)

		self.destination_x = new_x
		self.acceleration_x = self.movement_acceleration

		if new_x < self.x: # Moving left
			self.target_speed = -self.speed
		else: # Moving right
			self.target_speed = self.speed

	def go_to_tile_x(self, new_tile_x):
		self.go_to_x(new_tile_x * TILE_SIZE)

	def reset_to(self, x, y):
		super(SimpleAI, self).reset_to(x, y)

		self.destination_x = None

	def reset_to_tile(self, x, y):
		super(SimpleAI, self).reset_to_tile(x, y)

		self.destination_x = None



	def update(self, dt):
		super(SimpleAI, self).update(dt)

		if self.destination_x != None and ((self.target_speed < 0 and self.hitbox.x <= self.destination_x) or (self.target_speed > 0 and self.hitbox.x >= self.destination_x)):
			super(SimpleAI, self)._set_x(self.destination_x)

			self.destination_x = None
			self.target_speed = 0
