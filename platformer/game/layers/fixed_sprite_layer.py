import fixed_layer, sprite_layer

class FixedSpriteLayer(fixed_layer.FixedLayer, sprite_layer.SpriteLayer):
	"""A layer which contains a :class:`pyglet.sprite.Sprite` fixed relative to the viewport as its content."""

	def _update_graphic_coordinates(self, x, y, dt):
		self.graphic.set_position(self.viewport.x + self.offset_x, self.viewport.y + self.offset_y)
		self.graphic.update(dt)
