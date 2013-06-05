import linear

class EaseIn(linear.Linear):
	"""An easing transition which starts slow and gradually speeds up."""

	def __init__(self, *args, **kwargs):
		super(EaseIn, self).__init__(*args, **kwargs)

	def get_value_after_duration(self, elapsed_time):
		if elapsed_time <= 0:
			return self.start

		return self.start + self._position_delta * pow(max(elapsed_time/self.duration, 0), self.ease_power)
