import unittest
from ..util.image import dummy_image
from ..util.layers import assert_layer_factory
from ...layers import image_layer

class TestImageLayer(unittest.TestCase):

	def setUp(self):
		self.graphic = None
		self.layer = None

	expected_classes = {
		'default': image_layer.ImageLayer,
		'fixed': image_layer.FixedImageLayer,
		'static': image_layer.StaticImageLayer,
		'static-fixed': image_layer.FixedStaticImageLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of an image layer via the layer factory."""
		self.graphic = dummy_image(3,4)

		assert_layer_factory(self, 'image')
