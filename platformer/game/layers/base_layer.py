from pyglet.clock import schedule_once
from pyglet.event import EventDispatcher

class BaseLayer(EventDispatcher):
	"""A layer of graphical content.

	This class is used for determining how graphical contents should be
	drawn and in what order they should be drawn by a
	:class:`game.layers.LayerManager` object.

	If a duration is given, the layer will delete itself after that
	amount of time.

	Callbacks can be registered for this class's ``on_delete`` event.
	All registered ``on_delete`` callbacks should accept the layer
	as their only argument.

	Attributes:
		graphic (object): The graphical content.
		viewport (object): The viewport that this layer is drawn to.
	"""

	def __init__(self, graphic, viewport=None, duration=None):
		"""Creates a new layer.

		Args:
			graphic (object): The graphics content.

		Kwargs:
			viewport: The viewport that the layer is drawn to.
			duration (float): The number of seconds before this layer deletes itself.
		"""
		self.graphic = graphic
		self.viewport = viewport

		if duration:
			schedule_once(self._handle_duration_end, duration)

	def delete(self):
		"""Deletes the layer.

		An ``on_delete`` event is also fired.
		All registered ``on_delete`` callbacks should accept
		the layer as their only argument.
		"""
		self.graphic = None
		self.viewport = None
		self.dispatch_event('on_delete', self)

	def _handle_duration_end(self, dt):
		"""Deletes the layer after its duration has elapsed.

		Args:
			dt (float): The number of seconds that elapsed before this method was called.
		"""
		self.delete()

# Register layer events
BaseLayer.register_event_type('on_delete')
