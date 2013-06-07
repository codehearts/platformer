from base_layer import BaseLayer

# TODO Subclassing BaseLayer might be unnecessary
class FixedLayer(BaseLayer):
	"""Parent class for layers which wish to remain fixed to the viewport.

	This class is not intended for direct use. Any layers wishing to remain
	fixed to the viewport should subclass this class and either call
	``self.fix_graphic`` where appropriate or use
	``viewport.x + self.offset_x`` and ``viewport.y + self.offset_y`` as
	its coordinates.

	If using multiple inheritance to subclass this class, FixedLayer should
	be listed first.

	Attributes:
		offset_x (int): The number of pixels that the graphical content is horizontally offset by from the viewport's anchor point (usually the bottom left corner).
		offset_y (int): The number of pixels that the graphical content is vertically offset by from the viewport's anchor point (usually the bottom left corner).
	"""

	def __init__(self, *args, **kwargs):
		"""
		Kwargs:
			offset_x (int): The number of pixels to horizontally offset the graphical content from the viewport's anchor point (usually the bottom left corner).
			offset_y (int): The number of pixels to vertically offset the graphical content from the viewport's anchor point (usually the bottom left corner).
		"""
		# Get subclass kwargs with kwargs.pop to prevent passing them to parent
		self.offset_x = int(kwargs.pop('offset_x', 0))
		self.offset_y = int(kwargs.pop('offset_y', 0))

		super(FixedLayer, self).__init__(*args, **kwargs)

	def fix_graphic(self):
		"""Fixes the layer's graphical content to its viewport.
		"""
		# TODO Set invisible if the graphic is off the viewport
		self.graphic.x = self.viewport.x + self.offset_x
		self.graphic.y = self.viewport.y + self.offset_y
