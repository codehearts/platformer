import unittest
import pyglet.app
from game.animation import BasicAnimation
from game.easing import Linear, EaseOut, EaseIn
from game.util import floats_equal
from game.settings.general_settings import FPS, FRAME_LENGTH
from pyglet.clock import schedule_once
from util.image import dummy_image

class TestAnimations(unittest.TestCase):

	def setUp(self):
		self.animation = None



	def test_animation_creation(self):
		"""Tests creating an animation from an image."""
		rows = 4
		cols = 6
		image = dummy_image(rows, cols)
		duration = 10
		times = Linear.get_frame_durations(rows*cols, duration)

		# Create an animation with no delay which loops once
		self.animation = BasicAnimation.from_image(
			image, rows, cols, times
		)

		self.assertEqual(rows*cols, self.animation.frame_count,
			"Animation has wrong number of frames.")
		self.assertEqual(self.animation.current_frame_index, 0,
			"Animation began on wrong frame.")
		self.assertEqual(self.animation.elapsed_time, 0,
			"Animation began with non-zero elapsed time.")
		self.assertFalse(self.animation.is_infinite,
			"Animation was incorrectly created as infinite.")
		self.assertEqual(self.animation.total_loops, 1,
			"Animation has wrong number of loops.")
		self.assertEqual(self.animation.current_loop, 1,
			"Animation began on wrong loop.")
		self.assertEqual(self.animation.total_duration, duration,
			"Animation has wrong total duration.")
		self.assertFalse(self.animation.is_finished,
			"Animation claims to be finished after intialization.")

		# Create an animation with delay which loops once
		self.animation = BasicAnimation.from_image(
			image, rows, cols, times, delay=5
		)

		self.assertEqual(duration+5, self.animation.total_duration,
			"Animation's total duration did not include delay.")

		# Create an animation with no delay which loops multiple times
		self.animation = BasicAnimation.from_image(
			image, rows, cols, times, loops=5
		)

		self.assertEqual(duration*5, self.animation.total_duration,
			"Animation's total duration did not account for loops.")

		# Create an animation with delay which loops multiple times
		self.animation = BasicAnimation.from_image(
			image, rows, cols, times, loops=5, delay=5
		)

		self.assertEqual(duration*5+5, self.animation.total_duration,
			"Animation's total duration did not account for loops and delay.")

		# Create an animation with no delay which loops infinitely
		self.animation = BasicAnimation.from_image(
			image, rows, cols, times, loops=True
		)

		self.assertIs(None, self.animation.total_duration,
			"Animation has a total duration set with infinite loops.")

		# Create an animation with delay which loops infinitely
		self.animation = BasicAnimation.from_image(
			image, rows, cols, times, loops=True, delay=10
		)

		self.assertIs(None, self.animation.total_duration,
			"Animation has a total duration set with infinite loops and delay.")

	def test_animations(self):
		"""Ensures that animations play correctly."""
		self.tests_to_run = [
			{
				'name': 'No delay, 1 loop, linear curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 3,
					'cols': 4,
					'duration': 10,
					'easing_class': Linear,
				},
			},
			{
				'name': 'Delay, 1 loop, linear curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 3,
					'cols': 4,
					'duration': 10,
					'easing_class': Linear,
					'delay': 0.5,
				},
			},
			{
				'name': 'No delay, 3 loops, linear curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 3,
					'cols': 4,
					'duration': 10,
					'easing_class': Linear,
					'loops': 3,
				},
			},
			{
				'name': 'Delay, 3 loops, linear curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 5,
					'cols': 2,
					'duration': 5,
					'easing_class': Linear,
					'delay': 2.5,
					'loops': 3,
				},
			},
			{
				'name': 'No delay, 1 loop, ease out curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 3,
					'cols': 4,
					'duration': 7,
					'easing_class': EaseOut,
				},
			},
			{
				'name': 'Delay, 1 loop, ease in curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 3,
					'cols': 4,
					'duration': 10,
					'easing_class': EaseIn,
					'delay': 0.5,
				},
			},
			{
				'name': 'No delay, 3 loops, ease out curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 3,
					'cols': 4,
					'duration': 10,
					'easing_class': EaseOut,
					'loops': 3,
				},
			},
			{
				'name': 'Delay, 3 loops, ease in curve.',
				'fn': self.assert_animation,
				'args': {
					'rows': 5,
					'cols': 2,
					'duration': 5,
					'easing_class': EaseIn,
					'delay': 2.5,
					'loops': 3,
				},
			},
		]

		# Run pyglet to allow testing events
		schedule_once(self.run_animation_tests, 0)
		pyglet.app.run()



	def run_animation_tests(self, dt):
		"""Runs the animation tests queue.

		Intended for use within a running pyglet app.
		``pyglet.app.run()`` should be called before calling this.
		"""
		for test in self.tests_to_run:
			self.rows = test['args']['rows']
			self.cols = test['args']['cols']
			self.duration = test['args']['duration']
			self.easing_class = test['args']['easing_class']
			self.delay = test['args'].pop('delay', 0)
			self.loops = test['args'].pop('loops', 1)

			test['fn'](test['name'])

		pyglet.app.exit()



	def assert_animation(self, test_name):
		"""Asserts that an animation plays correctly.

		This test ensures that each frame is displayed for the optimal
		amount of time (is never displayed more than two frames longer or
		shorter than its expected time). Also checks whether events are
		firing when they should be."""
		# Create frame images and get frame times on the easing curve
		image = dummy_image(self.rows, self.cols)
		self.times = self.easing_class.get_frame_durations(
			self.rows * self.cols, self.duration
		)

		# Create the animation
		self.animation = BasicAnimation.from_image(
			image, self.rows, self.cols, self.times,
			delay=self.delay, loops=self.loops
		)

		# Set event handlers
		self.frame_change_fired = False
		self.animation_end_fired = False
		self.animation.set_handler(
			'on_frame_change', self.frame_change_handler
		)
		self.animation.set_handler(
			'on_animation_end', self.animation_end_handler
		)

		# Create a list of the amounts of time that are expected to pass
		# before each frame is displayed
		frame_change_times = [self.delay]
		for i in xrange(1, len(self.times) * self.loops):
			frame_change_times.append(
				self.times[i % len(self.times)-1] + frame_change_times[i-1]
			)

		current_frame = 0 # Index of the current frame
		current_loop = 1 # Current animation loop
		elapsed_time = 0 # Total elapsed time
		frame_time = 0 # Time spent on the current frame
		last_frame = 0 # The last frame that was displayed

		# Loop for however many frames are in the total duration,,
		# ignoring the first frame
		last_i = int(self.animation.total_duration * FPS) - 1
		for i in xrange(last_i + 1):
			self.animation.update(FRAME_LENGTH)

			# Update the elapsed time and time spent on the current frame
			elapsed_time += FRAME_LENGTH
			frame_time += FRAME_LENGTH

			# If the animation's frame changed
			if last_frame != self.animation.current_frame_index:
				# Advance the current frame, accounting for loops
				current_frame += 1
				if current_frame == self.animation.frame_count:
					current_loop += 1
					current_frame = 0

				frame_time = 0

				# assertAlmostEqual because the frame rate of the app
				# prevents animation frame changes from occuring exactly
				# when they are expected
				change_index = (current_loop-1) * len(self.times) + current_frame
				self.assertAlmostEqual(
					frame_change_times[change_index],
					elapsed_time,
					delta = FRAME_LENGTH,
					msg="Animation frame didn't change at expected time. "+test_name
				)

				# Ensure that a frame change event fired
				self.assertTrue(self.frame_change_fired,
					"Frame change did not fire event. "+test_name)
				self.frame_change_fired = False
			else:
				# Ensure that a frame change event did not fire
				self.assertFalse(self.frame_change_fired,
					"Frame change event fired when frame didn't change. "+test_name)

			# If this is not the last test iteration, ensure that the
			# animation's properties are correct
			if i != last_i:
				self.assertEqual(current_frame, self.animation.current_frame_index,
					"Current animation frame didn't update to proper value."+test_name)
				self.assertEqual(elapsed_time, self.animation.elapsed_time,
					"Animation has wrong elapsed time. "+test_name)
				self.assertEqual(current_loop, self.animation.current_loop,
					"Animation is on wrong loop. "+test_name)
				self.assertFalse(self.animation_end_fired,
					"Animation end event fired before it ended. "+test_name)
			# If this is the last test iteration, ensure that the
			# animation knows that it has finished
			else:
				self.assertTrue(self.animation.is_finished,
					"is_finished is False after last frame. "+test_name)
				self.assertTrue(
					floats_equal(
						self.animation.total_duration,
						self.animation.elapsed_time
					),
					"Animation did not last for specified duration. "+test_name)
				self.assertTrue(self.animation_end_fired,
					"Animation end event did not fire when it ended. "+test_name)

			# Update the index of the last frame we were on
			last_frame = self.animation.current_frame_index

	def frame_change_handler(self, animation):
		"""Handles an ``on_frame_change`` event from the animation."""
		self.frame_change_fired = True

	def animation_end_handler(self, animation):
		"""Handles an ``on_animation_end`` event from the animation."""
		self.animation_end_fired = True
