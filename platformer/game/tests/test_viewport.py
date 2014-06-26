from game.settings.general_settings import FPS, FRAME_LENGTH
from game.bounded_box import BoundedBox
from game.viewport import Viewport
import unittest

class TestViewport(unittest.TestCase):
	"""Tests the :class:`game.viewport.Viewport` class."""

	def test_viewport_bounding(self):
		"""Test bounding a viewport within specified boundaries."""
		# Test with bounds
		bounds = BoundedBox(-50, -50, 100, 100)
		viewport = Viewport(0, 0, 30, 40, bounds=bounds)

		self.assertEqual(viewport.x, 0,
			"Viewport did not initialize on correct x coordinate.")
		self.assertEqual(viewport.y, 0,
			"Viewport did not initialize on correct y coordinate.")

		viewport.focus_on_coordinates(-100, -100, duration=0.5)

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		self.assertEqual(viewport.x, bounds.x,
			"Viewport was not bounded after crossing left boundary.")
		self.assertEqual(viewport.y, bounds.y,
			"Viewport was not bounded after crossing lower boundary.")

		viewport.focus_on_coordinates(100, 100, duration=0.5)

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		self.assertEqual(viewport.x, bounds.x2 - viewport.width,
			"Viewport was not bounded after crossing right boundary.")
		self.assertEqual(viewport.y, bounds.y2 - viewport.height,
			"Viewport was not bounded after crossing upper boundary.")

		# Test without bounds
		viewport = Viewport(0, 0, 30, 40)

		self.assertEqual(viewport.x, 0,
			"Unbounded viewport did not initialize on correct x coordinate.")
		self.assertEqual(viewport.y, 0,
			"Unbounded viewport did not initialize on correct y coordinate.")

		viewport.focus_on_coordinates(-100, -100, duration=0.5)

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		self.assertEqual(viewport.x, -100,
			"Unbounded viewport did not move to new x coordinate.")
		self.assertEqual(viewport.y, -100,
			"Unbounded viewport did not move to new y coordinate.")

		viewport.focus_on_coordinates(100, 100, duration=0.5)

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		self.assertEqual(viewport.x, 100,
			"Unbounded viewport did not move to new x coordinate.")
		self.assertEqual(viewport.y, 100,
			"Unbounded viewport did not move to new y coordinate.")
