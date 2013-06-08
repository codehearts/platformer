import unittest
from game.animation import BasicAnimation
from ..util.image import dummy_image
from ..util.layers import assert_layer_factory
from ...layers import animation_layer

class TestAnimationLayer(unittest.TestCase):

	def setUp(self):
		self.graphic = None
		self.layer = None

	expected_classes = {
		'default': animation_layer.AnimationLayer,
		'fixed': animation_layer.FixedAnimationLayer,
		'static': animation_layer.AnimationLayer,
		'static-fixed': animation_layer.FixedAnimationLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of an animation layer via the layer factory."""
		times = [0.1] * (3*4)
		self.graphic = BasicAnimation.from_image(dummy_image(3,4), 3, 4, times)

		assert_layer_factory(self, 'animation')
