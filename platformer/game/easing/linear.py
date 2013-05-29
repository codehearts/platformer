class Linear(object):
	"""An easing transition which moves at a constant rate.

	Attributes:
		start (number): The starting value of the transition.
		end (number): The final value of the transition.
		duration (number): The amount of time (in seconds) that the transition will last for.
		ease_power (number): Determines how steep the easing curve will be. Higher values create steeper curves.
		elapsed_time (number): The amount of time that has elapsed since the easing transition began.
		current_value (number): The current value of the easing transition.
	"""

	def __init__(self, start, end, duration, ease_power=2):
		"""Creates a new easing transition.

		Args:
			start (number): The starting value of the transition.
			end (number): The final value of the transition.
			duration (number): The amount of time (in seconds) that the transition will last for.

		Kwargs:
			ease_power (number): Determines how steep the easing curve will be. Higher values create steeper curves.
		"""
		self.start = start
		self.end = end
		self.duration = float(duration)
		self.ease_power = ease_power
		self._position_delta = end - start # Used in easing calculations

		self.elapsed_time = 0
		self.current_value = start

		# When calling get_frame_durations from an instance of this class, pass the instance's data
		self._class_get_frame_durations = self.get_frame_durations
		self.get_frame_durations = self._instance_get_frame_durations

	def get_value(self):
		"""Returns the current value of the easing transition.

		Returns:
			The current value of the easing transition.
		"""
		return self.current_value

	# TODO Test that this is truly linear
	def get_value_after_duration(self, elapsed_time):
		"""Calculates the value of the easing transition after the specified amount of time.

		Args:
			elapsed_time (number): The amount of time to get the value of the easing transition after.

		Returns:
			The value of the easing transition after the specified amount of time.
		"""
		return self.start + self._position_delta * min(elapsed_time/self.duration, 1)

	def update(self, dt):
		"""Updates the easing transition to reflect the current position in time.

		Args:
			dt (number): The time delta (in seconds) between the current frame and the previous frame.
		"""
		self.elapsed_time += dt
		self.current_value = self.get_value_after_duration(self.elapsed_time)

	def _instance_get_frame_durations(self, frame_count):
		"""Calls :func:`get_frame_durations` on the current instance of the class.

		Args:
			frame_count (number): The number of frames to calculate the durations for.

		Returns:
			A list of floats representing the durations (in seconds) for each frame.
		"""
		return self._class_get_frame_durations(frame_count, self.duration, ease_power=self.ease_power)

	# TODO Write tests for this method! Check that sum(durations) is approximately the requested duration
	# TODO Test that this method works when called from a class and when called from an instance
	@classmethod
	def get_frame_durations(cls, frame_count, duration, ease_power=2):
		"""Calculates the amount of time that each frame in an animation should be displayed with this easing transition.

		Args:
			frame_count (number): The number of frames to calculate the durations for.
			duration (number): The total amount of time (in seconds) that the animation will last for.

		Kwargs:
			ease_power (number): Determines how steep the easing curve will be. Higher values create steeper curves.

		Returns:
			A list of floats representing the durations (in seconds) for each frame.
		"""
		duration = float(duration)
		easing = cls(0, duration, frame_count, ease_power=ease_power)
		frame_durations = []
		elapsed_time = 0

		for frame in xrange(frame_count):
			frame_durations.append((easing.get_value_after_duration(frame+1) - elapsed_time) / duration)
			elapsed_time += frame_durations[frame]

		return frame_durations
