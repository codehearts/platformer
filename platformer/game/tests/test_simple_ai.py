import pyglet, unittest
from game import load, util
from game.settings import general_settings, demo_settings

class TestSimpleAI(unittest.TestCase):
	
	# Tests the horizontal movement of simple AI
	def test_horizontal_movement(self):
		# flat_map is 100 tiles of floor
		flat_map = [[1]*100]
		flat_level = load.Stage(demo_settings.TILE_DATA, flat_map)
		character = load.single_character('test_object_6', 0, 1, flat_level.get_tiles()) # test_object_6 is a SimpleAI object
		
		
		
		# Tell it to move right to 50
		character.go_to_x(50)
		
		# Simulate 1 second of game time
		for i in range(int(general_settings.FPS)):
			character.update(general_settings.FRAME_LENGTH)
		
		# The object should be where we told it to go
		self.assertEqual((50, general_settings.TILE_SIZE), character.get_coordinates())
		
		
		
		# Tell it to move left to 25
		character.go_to_x(25)
		
		# Simulate 1 second of game time
		for i in range(int(general_settings.FPS)):
			character.update(general_settings.FRAME_LENGTH)
		
		# The object should be where we told it to go
		self.assertEqual((25, general_settings.TILE_SIZE), character.get_coordinates())
		
		
		
		# Tell it to move right to 100
		character.go_to_x(100)
		
		# Simulate 0.1 seconds of game time
		for i in range(int(general_settings.FPS * 0.1)):
			character.update(general_settings.FRAME_LENGTH)
		
		# The object shouldn't be where we told it to go yet, but it should be moving in that direction
		self.assertTrue(25 < character.get_coordinates()[0])
		self.assertTrue(100 > character.get_coordinates()[0])
		
		
		
		# Interupt the object to tell it to instead move to tile 5 (at this point it's still moving to 100)
		character.go_to_tile_x(5)
		
		# Simulate 2 seconds of game time
		for i in range(int(general_settings.FPS * 2)):
			character.update(general_settings.FRAME_LENGTH)
		
		# The object should be where we told it to go
		self.assertEqual((5*general_settings.TILE_SIZE, general_settings.TILE_SIZE), character.get_coordinates())
		
		
		
		# Tell it to move left to tile 2
		character.go_to_tile_x(2)
		
		# Simulate 1 second of game time
		for i in range(int(general_settings.FPS)):
			character.update(general_settings.FRAME_LENGTH)
		
		# The object should be where we told it to go
		self.assertEqual((2*general_settings.TILE_SIZE, general_settings.TILE_SIZE), character.get_coordinates())
		
		
		
		# Tell it to move right to tile 50
		character.go_to_tile_x(50)
		
		# Simulate 0.1 seconds of game time
		for i in range(int(general_settings.FPS * 0.1)):
			character.update(general_settings.FRAME_LENGTH)
		
		# The object shouldn't be where we told it to go yet, but it should be moving in that direction
		self.assertTrue(2*general_settings.TILE_SIZE < character.get_coordinates()[0])
		self.assertTrue(50*general_settings.TILE_SIZE > character.get_coordinates()[0])