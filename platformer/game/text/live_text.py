import text

class LiveText(text.Text):
	"""A text label which updates its contents with the return value of a function.

	Attributes:
		get_text_source (function): The source of the label's contents.
	"""

	def __init__(self, get_text_source, *args, **kwargs):
		"""Creates a new live text label that updates its contents with the return value of ``get_text_source``.

		Args:
			get_text_source (function): A function which returns the contents for the text label when the label is updated.
		"""
		super(LiveText, self).__init__(*args, **kwargs)

		self.get_text_source = get_text_source

	def update(self, *args, **kwargs):
		"""Updates the label with the returned value of the text source function."""
		self.text = self.get_text_source()

		super(LiveText, self).update(*args, **kwargs)
