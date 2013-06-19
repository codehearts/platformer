import unittest
from game.viewport import Viewport
from game.bounded_box import BoundedBox

class TestViewport(unittest.TestCase):
	"""Tests the :class:`game.viewport.Viewport` class."""

	def setUp(self):
		pass



	def test_viewport_bounding(self):
		"""Test bounding a viewport within specified boundaries."""
		# Test with bounds
		bounds = BoundedBox(-50, -50, 100, 100)
		self.viewport = Viewport(0, 0, 30, 40, bounds=bounds)

		self.assertEqual(self.viewport.x, 0,
			"Viewport did not initialize on correct x coordinate.")
		self.assertEqual(self.viewport.y, 0,
			"Viewport did not initialize on correct y coordinate.")

		self.viewport.update(1, -100, -100)

		self.assertEqual(self.viewport.x, bounds.x,
			"Viewport was not bounded after crossing left boundary.")
		self.assertEqual(self.viewport.y, bounds.y,
			"Viewport was not bounded after crossing lower boundary.")

		self.viewport.update(1, 100, 100)

		self.assertEqual(self.viewport.x, bounds.x2 - self.viewport.width,
			"Viewport was not bounded after crossing right boundary.")
		self.assertEqual(self.viewport.y, bounds.y2 - self.viewport.height,
			"Viewport was not bounded after crossing upper boundary.")

		# Test without bounds
		self.viewport = Viewport(0, 0, 30, 40)

		self.assertEqual(self.viewport.x, 0,
			"Unbounded viewport did not initialize on correct x coordinate.")
		self.assertEqual(self.viewport.y, 0,
			"Unbounded viewport did not initialize on correct y coordinate.")

		self.viewport.update(1, -100, -100)

		self.assertEqual(self.viewport.x, -100,
			"Unbounded viewport did not move to new x coordinate.")
		self.assertEqual(self.viewport.y, -100,
			"Unbounded viewport did not move to new y coordinate.")

		self.viewport.update(1, 100, 100)

		self.assertEqual(self.viewport.x, 100,
			"Unbounded viewport did not move to new x coordinate.")
		self.assertEqual(self.viewport.y, 100,
			"Unbounded viewport did not move to new y coordinate.")
