from pyglet.text import Label
from pyglet.clock import schedule_once

# TODO Should this be an HTMLLabel subclass instead of a Label subclass?
class Text(Label):

	def __init__(self, *args, **kwargs):
		# Get subclass kwargs with kwargs.pop to prevent passing them to parent
		self.duration = kwargs.pop('duration', None)

		super(Text, self).__init__(*args, **kwargs)

		if self.duration:
			schedule_once(self.handle_duration_end, self.duration)

	def update(self, x=None, y=None):
		if x: self.x = x
		if y: self.y = y

	# TODO Free up the memory this object was using
	def handle_duration_end(self, dt):
		self.delete() # Remove this label from its batch
