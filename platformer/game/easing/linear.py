class Linear(object):
	"""An easing transition which moves at a constant rate.

	Attributes:
		start (float): The starting value of the transition.
		end (float): The final value of the transition.
		duration (float): The amount of time (in seconds) that the transition will last for.
		ease_power (float): Determines how steep the easing curve will be. Higher values create steeper curves.
		elapsed_time (float): The amount of time that has elapsed since the easing transition began.
		value (float): The current value of the easing transition.
	"""

	def __init__(self, start, end, duration, ease_power=2):
		"""Creates a new easing transition.

		Args:
			start (float): The starting value of the transition.
			end (float): The final value of the transition.
			duration (float): The number of seconds that the transition will last for.

		Kwargs:
			ease_power (number): Determines how steep the easing curve will be. Higher values create steeper curves.
		"""
		self.start = start
		self.end = end
		self.duration = float(duration)
		self.ease_power = ease_power
		self._position_delta = end - start # Used in easing calculations

		self.elapsed_time = 0
		self.value = start

		# When calling get_frame_durations from an instance of this class, pass the instance's data
		self._class_get_frame_durations = self.get_frame_durations
		self.get_frame_durations = self._get_instance_frame_durations

	def get_value_after_duration(self, elapsed_time):
		"""Calculates the value of the easing transition after
		the specified amount of time.

		Args:
			elapsed_time (float): The number of seconds to get the value of the easing transition after.

		Returns:
			The value of the easing transition after the specified amount of time.
		"""
		if elapsed_time <= 0:
			return self.start

		return self.start + self._position_delta * min(elapsed_time/self.duration, 1)

	def update(self, dt):
		"""Updates the easing transition to reflect the current
		position in time.

		Args:
			dt (float): The number of seconds between the current frame and the previous frame.
		"""
		self.elapsed_time += dt
		self.value = self.get_value_after_duration(self.elapsed_time)

	def _get_instance_frame_durations(self, frame_count):
		"""Calls :func:`get_frame_durations` on the current instance of the class.

		Args:
			frame_count (int): The number of frames to calculate the durations for.

		Returns:
			A list of floats representing the durations (in seconds) for each frame.
		"""
		return self._class_get_frame_durations(frame_count, self.duration, ease_power=self.ease_power)



	@classmethod
	def get_frame_durations(cls, frame_count, duration, ease_power=2):
		"""Calculates the amount of time that each frame in an animation should be displayed with this easing transition.

		Args:
			frame_count (int): The number of frames to calculate the durations for.
			duration (float): The total number of seconds that the animation will last for.

		Kwargs:
			ease_power (float): Determines how steep the easing curve will be. Higher values create steeper curves.

		Returns:
			A list of floats representing the durations (in seconds) for each frame.
		"""
		duration = float(duration)
		easing = cls(0, duration, frame_count, ease_power=ease_power)
		last_value = easing.get_value_after_duration(0)
		frame_durations = []

		for frame in xrange(frame_count):
			# Storing values this way means we only calculate the
			# value for each frame once and then store it until
			# we don't need it anymore
			value = easing.get_value_after_duration(frame+1)

			frame_durations.append(value - last_value)
			last_value = value

		return frame_durations
