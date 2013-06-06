from text import Text

# TODO What's the point of this class? It functions almost exactly as text.Text
class Heading(Text):
	"""A text label intended for headings."""

	def __init__(self, *args, **kwargs):
		# Set the default font size to 18
		if not 'font_size' in kwargs:
			kwargs['font_size'] = 18

		super(Heading, self).__init__(*args, **kwargs)
