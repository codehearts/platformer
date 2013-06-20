import unittest
from pyglet.sprite import Sprite
from ..util.image import dummy_image
from ..util.layers import assert_layer_factory
from ...layers import graphics_layer

class TestGraphicsLayer(unittest.TestCase):
	"""Tests the base layer class."""

	def setUp(self):
		self.graphic = None
		self.layer = None

	expected_classes = {
		'default': graphics_layer.GraphicsLayer,
		'fixed': graphics_layer.FixedGraphicsLayer,
		'static': graphics_layer.StaticGraphicsLayer,
		'static-fixed': graphics_layer.FixedStaticGraphicsLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of a graphic layer via the layer factory."""
		self.graphic = Sprite(dummy_image(3,4))

		assert_layer_factory(self, 'graphics')
