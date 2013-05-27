import text

class LiveText(text.Text):

	def __init__(self, get_text_source, *args, **kwargs):
		super(LiveText, self).__init__(*args, **kwargs)

		self.get_text_source = get_text_source

	def update(self, *args, **kwargs):
		self.text = self.get_text_source()

		super(LiveText, self).update(*args, **kwargs)
