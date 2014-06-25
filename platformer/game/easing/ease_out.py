import linear

class EaseOut(linear.Linear):
	"""An easing transition which starts fast and gradually slows down."""

	def __init__(self, *args, **kwargs):
		super(EaseOut, self).__init__(*args, **kwargs)

	def get_value_after_duration(self, elapsed_time):
		if elapsed_time <= 0:
			return self.start
		elif elapsed_time >= self.duration:
			return self.end

		return self.start + self._position_delta * (1 - pow(1 - min(elapsed_time/self.duration, 1), self.ease_power))
