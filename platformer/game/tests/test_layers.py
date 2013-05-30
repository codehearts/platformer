import pyglet, unittest
from game.animation.tiled_animation import TiledAnimation
from game.text.text import Text
from game import layers

# TODO Delete this class when viewport testing becomes less of a mess
class AnonymousObject(object):
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

class TestLayerFactory(unittest.TestCase):

	def setUp(self):
		# TODO In the future, I'd like to be able to test with an actual viewport object that doesn't require a character and stage object
		self.viewport = AnonymousObject(x=0, y=0, width=800, height=600)

		# TODO Load a physical object
		#self.physical_object =

		self.text = Text('Test Label')

		animation_image = pyglet.resource.image('transition.png')
		animation_image_rows = 1
		animation_image_cols = 31
		animation_durations = [1] * (animation_image_rows * animation_image_cols)

		self.sprite = pyglet.sprite.Sprite(animation_image)

		self.animation = TiledAnimation.from_image(
			animation_image,
			animation_image_rows,
			animation_image_cols,
			animation_durations,
			self.viewport.width,
			self.viewport.height
		)


	# TODO Test that durations and other attributes are being set properly
	def test_layer_factory(self):
		# Test creation of a basic layer
		returned_layer = layers.create_layer(None, self.viewport, fixed=False)
		self.assertEqual(type(returned_layer), layers.BasicLayer, "Layer factory failed to create a basic layer.")

		# Test creation of a fixed layer
		returned_layer = layers.create_layer(None, self.viewport, fixed=True)
		self.assertEqual(type(returned_layer), layers.FixedLayer, "Layer factory failed to create a fixed layer.")

		# TODO Enable this test when physical objects can be easily obtained
		# Test creation of a physical object layer
		#returned_layer = layers.create_layer(self.physical_object, self.viewport, fixed=False)
		#self.assertEqual(type(returned_layer), layers.PhysicalObjectLayer, "Layer factory failed to create a physical object layer.")

		# TODO Enable this test when physical objects can be easily obtained
		# Test creation of a "fixed" physical object layer (physical objects can not be fixed to the viewport)
		#returned_layer = layers.create_layer(self.physical_object, self.viewport, fixed=True)
		#self.assertEqual(type(returned_layer), layers.PhysicalObjectLayer, "Layer factory failed to create a physical object layer when specified as fixed.")

		# Test creation of a sprite layer
		returned_layer = layers.create_layer(self.sprite, self.viewport, fixed=False)
		self.assertEqual(type(returned_layer), layers.SpriteLayer, "Layer factory failed to create a sprite layer.")

		# Test creation of a fixed sprite layer
		returned_layer = layers.create_layer(self.sprite, self.viewport, fixed=True)
		self.assertEqual(type(returned_layer), layers.FixedSpriteLayer, "Layer factory failed to create a fixed sprite layer.")

		# TODO Enable this when TileMap is refactored
		# Test creation of a tile map layer
		#returned_layer = layers.create_layer(self.tile_map, self.viewport, fixed=False)
		#self.assertEqual(type(returned_layer), layers.TileMapLayer, "Layer factory failed to create a tile map layer.")

		# TODO Enable this when TileMap is refactored
		# Test creation of a fixed tile map layer
		#returned_layer = layers.create_layer(self.tile_map, self.viewport, fixed=True)
		#self.assertEqual(type(returned_layer), layers.FixedTileMapLayer, "Layer factory failed to create a fixed tile map layer.")

		# Test creation of a text layer
		returned_layer = layers.create_layer(self.text, self.viewport, fixed=False)
		self.assertEqual(type(returned_layer), layers.TextLayer, "Layer factory failed to create a text layer.")

		# Test creation of a fixed text layer
		returned_layer = layers.create_layer(self.text, self.viewport, fixed=True)
		self.assertEqual(type(returned_layer), layers.FixedTextLayer, "Layer factory failed to create a fixed text layer.")

		# Test creation of an animation layer
		returned_layer = layers.create_layer(self.animation, self.viewport, fixed=False)
		self.assertEqual(type(returned_layer), layers.AnimationLayer, "Layer factory failed to create an animation layer.")

		# Test creation of a fixed animation layer
		returned_layer = layers.create_layer(self.animation, self.viewport, fixed=True)
		self.assertEqual(type(returned_layer), layers.FixedAnimationLayer, "Layer factory failed to create a fixed animation layer.")
