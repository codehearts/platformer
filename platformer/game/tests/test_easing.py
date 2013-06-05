import unittest
from game.easing import Linear, EaseIn, EaseOut

class testEasing(unittest.TestCase):

	def setUp(self):
		self.easing = None
		self.ease_class = None
		self.durations = None
		self.expected_values = None
		self.expected_frame_durations = None

	def test_linear_curve(self):
		"""Tests that the proper values are returned on a linear curve."""
		self.ease_class = Linear

		# Linear curve from 1 to 2 in 10 time units
		self.easing = self.ease_class(1, 2, 10)
		self.durations = range(11)
		self.expected_values = [1 + x/10.0 for x in self.durations]

		# Assert that the easing values are exactly as expected
		self.assert_exact_easing_values()


		# Linear curve from 2 to 1 in 10 time units
		self.easing = self.ease_class(2, 1, 10)
		# Test with intermittent time values
		self.durations = range(21)
		self.expected_values = [2 - x/20.0 for x in self.durations]
		self.durations = [x/2.0 for x in self.durations]

		# Assert that the easing values are exactly as expected
		self.assert_exact_easing_values()


		# Linear curve from 2.5 to 37.5 in 20 time units
		self.easing = self.ease_class(2.5, 37.5, 20)
		self.durations = range(21)
		# 37.5-2.5 = 35, 35/20 = 1.75
		self.expected_values = [2.5 + 1.75*x for x in self.durations]

		# Assert that the easing values are exactly as expected
		self.assert_exact_easing_values()


		# Linear curve from 2.5 to 37.5 in 20 time units
		self.easing = self.ease_class(37.5, 2.5, 20)
		# Test with intermittent time values
		self.durations = range(41)
		# 37.5-2.5 = 35, 35/20 = 1.75, 1.75/2 = 0.875
		self.expected_values = [37.5 - 0.875*x for x in self.durations]
		self.durations = [x/2.0 for x in self.durations]

		# Assert that the easing values are exactly as expected
		self.assert_exact_easing_values()

	def test_linear_frame_durations(self):
		"""Tests frame durations on a linear curve."""
		self.ease_class = Linear

		# Total duration of 10 time units
		self.easing = self.ease_class(1, 2, 10)

		# Test durations for 10 frames
		self.expected_frame_durations = [1] * 10
		self.assert_exact_frame_durations()

		# Test durations for 20 frames
		self.expected_frame_durations = [0.5] * 20
		self.assert_exact_frame_durations()


		# Total duration of 25 time units
		self.easing = self.ease_class(2, 1, 25)

		# Test durations for 10 frames
		self.expected_frame_durations = [25/10.0] * 10
		self.assert_exact_frame_durations()

		# Test durations for 60 frames (the values will not be exact)
		self.expected_frame_durations = [25/60.0] * 60
		self.assert_approx_frame_durations()





	def test_ease_in_curve(self):
		"""Tests that the proper values are returned on an ease in curve."""
		self.ease_class = EaseIn

		# Ease in curve from 1 to 2 in 10 time units
		self.easing = self.ease_class(1, 2, 10, ease_power=2)

		# Ensure that the slope of the easing function is increasing
		# at a non-constant rate
		self.assert_ease_in()


		self.easing = self.ease_class(10, 0, 10, ease_power=1.5)
		self.assert_ease_in(decreasing=True)

		self.easing = self.ease_class(2.5, 37.5, 4, ease_power=5)
		self.assert_ease_in()

		self.easing = self.ease_class(37.5, 2.5, 20, ease_power=5)
		self.assert_ease_in(decreasing=True)



	def test_ease_out_curve(self):
		"""Tests that the proper values are returned on an ease out curve."""
		self.ease_class = EaseOut

		# Ease out curve from 1 to 2 in 10 time units
		self.easing = self.ease_class(1, 2, 10, ease_power=2)

		# Ensure that the slope of the easing function is decreasing
		# at a non-constant rate
		self.assert_ease_out()


		self.easing = self.ease_class(10, 0, 10, ease_power=1.5)
		self.assert_ease_out(decreasing=True)

		self.easing = self.ease_class(2.5, 37.5, 4, ease_power=5)
		self.assert_ease_out()

		self.easing = self.ease_class(37.5, 2.5, 20, ease_power=5)
		self.assert_ease_out(decreasing=True)





	def assert_exact_easing_values(self):
		"""Asserts that the easing values are exactly as expected."""
		self.assert_easing_values(self.assertEqual)

	def assert_approx_easing_values(self):
		"""Asserts that the easing values are approximately as expected."""
		self.assert_easing_values(self.assertAlmostEqual)

	def assert_easing_values(self, assert_fn, **kwargs):
		"""Tests easing values with the specified assertion function."""
		elapsed_time = 0
		for i in xrange(len(self.expected_values)):
			value = self.expected_values[i]
			time = self.durations[i]

			# Test get_value_after_duration
			assert_fn(
				self.easing.get_value_after_duration(time), value,
				msg="Easing curve has wrong value after specified duration.", **kwargs
			)

			# Test by updating the easing object with the time difference
			self.easing.update(time - elapsed_time)
			elapsed_time += time - elapsed_time

			# Ensure the easing curve's current value is correct
			assert_fn(
		# Test with intermittent time values
				self.easing.value, value,
				msg="Easing curve has wrong value after update.", **kwargs
			)


		# Ensure that the curve never passes the start and end values
		assert_fn(
			self.easing.start, self.easing.get_value_after_duration(-50),
			msg="Easing curve does not stop at start value.", **kwargs
		)
		assert_fn(
			self.easing.end,
			self.easing.get_value_after_duration(self.durations[-1] * 2),
			msg="Easing curve does not stop at end value.", **kwargs
		)



	def assert_exact_frame_durations(self):
		"""Asserts that the frame durations for an easing curve are exactly as expected."""
		self.assert_frame_durations(self.assertEqual)

	def assert_approx_frame_durations(self):
		"""Asserts that the frame durations for an easing curve are approximately as expected."""
		self.assert_frame_durations(self.assertAlmostEqual)

	def assert_frame_durations(self, assert_fn, **kwargs):
		"""Tests frame durations for an easing curve with the specified assertion function."""
		class_list = self.ease_class.get_frame_durations(
			len(self.expected_frame_durations),
			self.easing.duration,
			self.easing.ease_power
		)

		instance_list = self.easing.get_frame_durations(
			len(self.expected_frame_durations)
		)

		self.assertEqual(
			class_list, instance_list,
			"Class and instance get_frame_durations values differed."
		)

		assert_fn(
			sum(class_list), self.easing.duration,
			msg="Total duration of frame lengths differs from easing duration.", **kwargs
		)

		for i in xrange(len(self.expected_frame_durations)):
			assert_fn(
				self.expected_frame_durations[i], class_list[i],
				msg="Frame duration for easing curve is wrong.",
				**kwargs
			)



	def assert_ease_in(self, decreasing=False):
		"""Asserts that the ease in function is monotonically increasing at a non-constant rate.

		Kwargs:
			decreasing (bool): Whether the easing function is decreasing (start value is greater than end value)
		"""
		self.assert_ease_in_or_out(ease_out=False, decreasing=decreasing)

	def assert_ease_out(self, decreasing=False):
		"""Asserts that the ease out function is monotonically decreasing at a non-constant rate.

		Kwargs:
			decreasing (bool): Whether the easing function is decreasing (start value is greater than end value)
		"""
		self.assert_ease_in_or_out(ease_out=True, decreasing=decreasing)

	def assert_ease_in_or_out(self, ease_out=False, decreasing=False):
		"""Asserts that the easing function is monotonically increasing or decreasing at a non-constant rate.

		Kwargs:
			ease_out (bool): Whether this is for ease out or ease in.
			decreasing (bool): Whether the easing function is decreasing (start value is greater than end value)
		"""
		if decreasing and not ease_out or ease_out and not decreasing:
			assert_fn = self.assertLess
		else:
			assert_fn = self.assertGreater

		if ease_out:
			name = 'Ease out '
			verb = ' monotonically slowing down '
		else:
			name = 'Ease in '
			verb = ' monotonically speeding up '

		last_slope = None
		last_value = self.easing.get_value_after_duration(0)
		for i in xrange(int(self.easing.duration)):
			value = self.easing.get_value_after_duration(i+1)
			slope = value - last_value

			if last_slope:
				assert_fn(slope, last_slope,
					name+'is not'+verb+'at a non-constant rate.'
				)

			last_value = value
			last_slope = slope
