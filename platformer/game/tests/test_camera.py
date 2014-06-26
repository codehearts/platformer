from game.settings.general_settings import TILE_SIZE, FPS, FRAME_LENGTH
from game.viewport import Camera
from game.bounded_box import BoundedBox
from game.easing import EaseIn, EaseOut
import unittest

class TestCamera(unittest.TestCase):
	"""Tests the camera to ensure that it controls the viewport correctly and focuses on the correct coordinates."""

	def test_target_focus(self):
		"""Tests focusing the camera on a target."""
		# 100 by 100 bounds
		bounds = BoundedBox(0, 0, 100*TILE_SIZE, 100*TILE_SIZE)

		# Target in the middle of bounds
		target = BoundedBox(50*TILE_SIZE, 50*TILE_SIZE, TILE_SIZE, TILE_SIZE)

		# 8 by 6 viewport which is requested to be out of bounds
		viewport = Camera(-8*TILE_SIZE, -6*TILE_SIZE, 8*TILE_SIZE, 6*TILE_SIZE, bounds=bounds, target=target)

		# Ensure that the camera focused on the target
		self.assertEqual(viewport.mid_x, target.mid_x, 'Camera did not focus on target x when initialized')
		self.assertEqual(viewport.mid_y, target.mid_y, 'Camera did not focus on target y when initialized')

		# Test initial target focus when bounded by the top and left of the stage

		# Move the target to the bottom left corner
		target.x = 0
		target.y = 0

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH) # Give the camera a full second to catch up

		# Because the target is at the bottom left corner of the bounds, the viewport should not cross those boundaries
		self.assertEqual(viewport.x, 0, 'Focusing on target x when bounded by stage left failed')
		self.assertEqual(viewport.y, 0, 'Focusing on target y when bounded by stage bottom failed')

		# Test target focus when bounded by the bottom of the bounds

		# Move the target horizontally so the camera is not bounded by the left bounds
		target.x = 25 * TILE_SIZE

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH) # Give the camera a full second to catch up

		# The viewport should be focusing on the center of the target, but still be bounded by the bottom of the bounds
		self.assertEqual(viewport.mid_x, target.mid_x, 'Focusing on target x when within horizontal bounds failed')
		self.assertEqual(viewport.y, 0, 'Focusing on target y when bounded by boundary bottom failed')

		# Test target focus when fully within bounds

		# Move the target so that the camera will be within bounds
		target.x = 25 * TILE_SIZE
		target.y = 25 * TILE_SIZE

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH) # Give the camera a full second to catch up

		# The viewport should be focusing on the center of the target
		self.assertEqual(viewport.mid_x, target.mid_x, 'Focusing on target x when within horizontal bounds failed')
		self.assertEqual(viewport.mid_y, target.mid_y, 'Focusing on target y when within vertical bounds failed')



	def test_alternating_focus(self):
		"""Tests focusing on and off of a target."""
		# 100 by 100 bounds
		bounds = BoundedBox(0, 0, 100*TILE_SIZE, 100*TILE_SIZE)

		# Target in the middle of bounds
		target = BoundedBox(0, 0, TILE_SIZE, TILE_SIZE)

		# 8 by 6 viewport
		viewport = Camera(0, 0, 8*TILE_SIZE, 6*TILE_SIZE, bounds=bounds, target=target)

		# Test moving focus to tile (20, 20) in 2 seconds with ease-in function

		viewport.focus_on_tile(20, 20, duration=2, easing=EaseIn)
		halfway_x = (20 * TILE_SIZE - viewport.mid_x) / 2.0 + viewport.mid_x
		halfway_y = (20 * TILE_SIZE - viewport.mid_y) / 2.0 + viewport.mid_y

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		# Since half the duration is up and we're using an ease in function, we should be less than halfway there
		self.assertTrue(viewport.mid_x < halfway_x, 'Camera is moving incorrectly with horizontal ease in after half of the duration')
		self.assertTrue(viewport.mid_y < halfway_y, 'Camera is moving incorrectly with vertical ease in after half of the duration')

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		# Since the duration is up, we should be at our destination (it actually falls short by a small fraction, which is acceptable)
		self.assertEqual(viewport.mid_x / TILE_SIZE, 19, 'Camera did not arrive at horizontal destination with ease in function')
		self.assertEqual(viewport.mid_y / TILE_SIZE, 19, 'Camera did not arrive at vertical destination with ease in function')

		# Test moving focus to tile (40, 40) in 2 seconds with ease-out function

		viewport.focus_on_tile(40, 40, duration=2, easing=EaseOut)
		halfway_x = (40 * TILE_SIZE - viewport.mid_x) / 2.0 + viewport.mid_x
		halfway_y = (40 * TILE_SIZE - viewport.mid_y) / 2.0 + viewport.mid_y

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		# Since half the duration is up and we're using an ease out function, we should be more than halfway there
		self.assertTrue(viewport.mid_x > halfway_x, 'Camera is moving incorrectly with horizontal ease out after half of the duration')
		self.assertTrue(viewport.mid_y > halfway_y, 'Camera is moving incorrectly with vertical ease out after half of the duration')

		# Simulate 1 second of time
		for i in xrange(int(FPS)):
			viewport.update(FRAME_LENGTH)

		# Since the duration is up, we should be at our destination
		self.assertEqual(viewport.mid_x / TILE_SIZE, 40, 'Camera did not arrive at horizontal destination with ease out function')
		self.assertEqual(viewport.mid_y / TILE_SIZE, 40, 'Camera did not arrive at vertical destination with ease out function')

		# Test moving focus back to the target in 1 second with an ease out function

		viewport.focus_on_target(duration=1, easing=EaseOut)

		# The target is at the bottom left of the stage, so the camera will be bounded by that
		halfway_x = (viewport.mid_x - viewport.half_width) / 2.0
		halfway_y = (viewport.mid_y - viewport.half_height) / 2.0

		# Simulate half a second of time
		for i in xrange(int(FPS * 0.5)):
			viewport.update(FRAME_LENGTH)

		# Since half the duration is up and we're using an ease out function, we should be more than halfway there
		self.assertTrue(viewport.mid_x < halfway_x, 'Camera is moving incorrectly back to target with horizontal ease out after half of the duration')
		self.assertTrue(viewport.mid_y < halfway_y, 'Camera is moving incorrectly back to target with vertical ease out after half of the duration')

		# Simulate half a second of time
		for i in xrange(int(FPS * 0.5)):
			viewport.update(FRAME_LENGTH)

		# Since the duration is up, we should be at our destination
		self.assertEqual(viewport.x, 0, 'Camera did not arrive at horizontal target coordinate with ease out function')
		self.assertEqual(viewport.y, 0, 'Camera did not arrive at vertical target coordinate with ease out function')
