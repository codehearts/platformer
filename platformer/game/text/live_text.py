import text

class LiveText(text.Text):
	"""A text label which updates its contents using a given function.

	Attributes:
		get_text_source: The function used in updating the label's contents.
	"""

	def __init__(self, get_text_source, *args, **kwargs):
		"""Creates a new live text label that updates its contents with the given function.

		Args:
			get_text_source (function): A function which provides the contents for the text label when it is updated.
		"""
		super(LiveText, self).__init__(*args, **kwargs)

		self.get_text_source = get_text_source

	def update(self, *args, **kwargs):
		"""Updates the label with the returned value of the text source function."""
		self.text = self.get_text_source()

		super(LiveText, self).update(*args, **kwargs)
