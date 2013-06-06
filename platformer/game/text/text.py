from pyglet.text import Label

# TODO Should this be an HTMLLabel subclass instead of a Label subclass?
class Text(Label):
	"""A text label."""

	def update(self, x=None, y=None):
		"""Updates the text label's positioning.

		Kwargs:
			x (number): The new x position for this label.
			y (number): The new y position for this label.
		"""
		if x:
			self.x = x
		if y:
			self.y = y
