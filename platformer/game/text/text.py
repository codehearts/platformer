from pyglet.text import Label

# TODO Should this be an HTMLLabel subclass instead of a Label subclass?
# TODO Does it really make sense for this class to support a duration?
class Text(Label):
	"""A text label."""

	def __init__(self, *args, **kwargs):
		"""Creates a new text label."""
		super(Text, self).__init__(*args, **kwargs)

	def update(self, x=None, y=None):
		"""Updates the text label's positioning.

		Kwargs:
			x (number): The new x position for this label.
			y (number): The new y position for this label.
		"""
		if x: self.x = x
		if y: self.y = y
