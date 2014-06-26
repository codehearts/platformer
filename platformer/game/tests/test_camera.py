import pyglet, unittest
from game import load
from game.viewport import Camera
from game.physical_objects.physical_object import PhysicalObject
from game.bounded_box import BoundedBox
from game.settings.general_settings import TILE_SIZE

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

		self.assertEqual(viewport.x, target.mid_x - viewport.half_width, 'Camera did not focus on target x when initialized')
		self.assertEqual(viewport.y, target.mid_y - viewport.half_height, 'Camera did not focus on target y when initialized')

		# flat_map is 100 tiles of floor with 19 rows of empty space above
		#flat_map = [[0]*100]*19 + [[1]*100]
		#flat_level = load.Stage(demo_settings.TILE_DATA, flat_map)
		#character = load.single_character('test_object_6', 0, 1, flat_level.get_tiles()) # test_object_6 is a SimpleAI object
		#game_window = pyglet.window.Window(800, 600, visible=False)

		# Load the camera and focus on our test object
		#cam = camera.Camera(character, game_window, flat_level.get_tiles())
		#cam.focus()

		# Test initial target focus when bounded by the top and left of the stage

		# Because the character started out at the bottom left of the stage, the camera will not cross those boundaries
		self.assertEqual(viewport.x, 0, 'Focusing on target x when bounded by stage left failed')
		self.assertEqual(viewport.y, 0, 'Focusing on target y when bounded by stage bottom failed')



		## Test target focus when bounded by the bottom of the stage

		#character.reset_to_tile(25, 1)
		#cam.update(general_settings.FRAME_LENGTH)

		## The camera should be focusing on the center of the test object, but still be bounded by the bottom of the stage
		#self.assertEqual(cam.focus_x, character.get_x()+character.get_half_width(), 'Focusing on target x when unbounded failed')
		#self.assertEqual(cam.focus_y, cam.half_height, 'Focusing on target y when bounded by stage bottom failed')



		## Test unbounded target focus

		#character.reset_to_tile(25, 10)
		#cam.update(general_settings.FRAME_LENGTH)

		## The camera should be focusing on the center of the test object
		#self.assertEqual(cam.focus_x, character.get_x()+character.get_half_width(), 'Focusing on target x when unbounded failed')
		#self.assertEqual(cam.focus_y, character.get_y()+character.get_half_height(), 'Focusing on target y when unbounded failed')


		#game_window.close()



	# Tests focusing on and off a target
	#def test_alternating_focus(self):
		## flat_map is 100 tiles of floor with 19 rows of empty space above
		#flat_map = [[0]*100]*19 + [[1]*100]
		#flat_level = load.Stage(demo_settings.TILE_DATA, flat_map)
		#character = load.single_character('test_object_6', 0, 1, flat_level.get_tiles()) # test_object_6 is a SimpleAI object
		#game_window = pyglet.window.Window(800, 600, visible=False)
		#tile_size = general_settings.TILE_SIZE_FLOAT

		## Load the camera and focus on our test object
		#cam = camera.Camera(character, game_window, flat_level.get_tiles())
		#cam.focus()



		## Test moving focus to tile (20, 20) in 2 seconds with ease-in function

		#cam.move_to_tile(20, 20, 2, general_settings.EASE_IN)
		#halfway_x = ((20*tile_size) - cam.focus_x) / 2.0 + cam.focus_x
		#halfway_y = ((20*tile_size) - cam.focus_y) / 2.0 + cam.focus_y

		## Simulate 1 second of game time
		#for i in xrange(int(general_settings.FPS)):
			#cam.update(general_settings.FRAME_LENGTH)

		## Since half the duration is up and we're using an ease-in function, we should be less than halfway there
		#self.assertTrue(cam.focus_x < halfway_x, 'Ease-in in x direction at half duration failed')
		#self.assertTrue(cam.focus_y < halfway_y, 'Ease-in in y direction at half duration failed')

		## Simulate 1 second of game time
		#for i in xrange(int(general_settings.FPS)):
			#cam.update(general_settings.FRAME_LENGTH)

		## Since the duration is up, we should be at our destination (it actually falls short by a small fraction, which is acceptable)
		#self.assertEqual(int(cam.focus_x/tile_size), 19, 'Ease-in did not arrive at x destination')
		#self.assertEqual(int(cam.focus_y/tile_size), 19, 'Ease-in did not arrive at y destination')



		## Test moving focus to tile (40, 40) in 2 seconds with ease-out function

		#cam.move_to_tile(40, 40, 2, general_settings.EASE_OUT)
		#halfway_x = ((40*tile_size) - cam.focus_x) / 2.0 + cam.focus_x
		#halfway_y = ((40*tile_size) - cam.focus_y) / 2.0 + cam.focus_y

		## Simulate 1 second of game time
		#for i in xrange(int(general_settings.FPS)):
			#cam.update(general_settings.FRAME_LENGTH)

		## Since half the duration is up and we're using an ease-out function, we should be more than halfway there
		#self.assertTrue(cam.focus_x > halfway_x, 'Ease-out in x direction at half duration failed')
		#self.assertTrue(cam.focus_y > halfway_y, 'Ease-out in y direction at half duration failed')

		## Simulate 1 second of game time
		#for i in xrange(int(general_settings.FPS)):
			#cam.update(general_settings.FRAME_LENGTH)

		## Since the duration is up, we should be at our destination
		#self.assertEqual(int(cam.focus_x/tile_size), 40, 'Ease-out did not arrive at x destination')
		#self.assertEqual(int(cam.focus_y/tile_size), 40, 'Ease-out did not arrive at y destination')



		## Test moving focus back to the target in 1 second with ease-out function

		#cam.focus_on_target(1, general_settings.EASE_OUT)

		## The target is at the bottom left of the stage, so the camera will be bounded by that
		#halfway_x = (cam.focus_x - cam.half_width) / 2.0
		#halfway_y = (cam.focus_y - cam.half_height) / 2.0

		## Simulate half a second of game time
		#for i in xrange(int(general_settings.FPS * 0.5)):
			#cam.update(general_settings.FRAME_LENGTH)

		## Since half the duration is up and we're using an ease-out function, we should be more than halfway there

		#self.assertTrue(cam.focus_x > halfway_x, 'Ease-out in x direction when refocusing on target at half duration failed')
		#self.assertTrue(cam.focus_y > halfway_y, 'Ease-out in y direction when refocusing on target at half duration failed')

		## Simulate half a second of game time
		#for i in xrange(int(general_settings.FPS * 0.5)):
			#cam.update(general_settings.FRAME_LENGTH)

		## Since the duration is up, we should be at our destination (it actually falls short by a small fraction, which is acceptable)

		#self.assertEqual(cam.focus_x, cam.half_width, 'Ease-out did not arrive at target')
		#self.assertEqual(cam.focus_y, cam.half_height, 'Ease-out did not arrive at target')


		#game_window.close()
