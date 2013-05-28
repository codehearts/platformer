from pyglet.text import Label
from pyglet.clock import schedule_once

# TODO Should this be an HTMLLabel subclass instead of a Label subclass?
# TODO Does it really make sense for this class to support a duration?
class Text(Label):
	"""A text label which can be displayed for a set duration of time.

	Attributes:
		duration: The number of seconds this text label will last for.
	"""

	def __init__(self, *args, **kwargs):
		"""Creates a new text label.

		Kwargs:
			duration: The number of seconds that the text label should last for.
		"""
		# Get subclass kwargs with kwargs.pop to prevent passing them to parent
		self.duration = kwargs.pop('duration', None)

		super(Text, self).__init__(*args, **kwargs)

		if self.duration:
			schedule_once(self.handle_duration_end, self.duration)

	def update(self, x=None, y=None):
		"""Updates the text label's positioning.

		Kwargs:
			x: The new x position for this label.
			y: The new y position for this label.
		"""
		if x: self.x = x
		if y: self.y = y

	# TODO Free up the memory this object was using
	def handle_duration_end(self, dt):
		"""Handles cleanup of this label when its duration has expired."""
		self.delete() # Remove this label from its batch
