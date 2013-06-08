import unittest
from game.text import Text
from ..util.layers import assert_layer_factory
from ...layers import text_layer

class TestTextLayer(unittest.TestCase):

	def setUp(self):
		self.graphic = None
		self.layer = None

	expected_classes = {
		'default': text_layer.TextLayer,
		'fixed': text_layer.FixedTextLayer,
		'static': text_layer.StaticTextLayer,
		'static-fixed': text_layer.FixedStaticTextLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of an text layer via the layer factory."""
		self.graphic = Text('Test')

		assert_layer_factory(self, 'text')
