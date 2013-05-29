import linear

class EaseIn(linear.Linear):
	"""An easing transition which starts fast and gradually slows down."""

	def __init__(self, *args, **kwargs):
		super(EaseIn, self).__init__(*args, **kwargs)

	def get_value_after_duration(self, elapsed_time):
		return self.start + self._position_delta * pow(max(elapsed_time/self.duration, 0), self.ease_power)
