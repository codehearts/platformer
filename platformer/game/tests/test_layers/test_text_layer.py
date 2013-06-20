import unittest
from game.text import Text, LiveText
from ..util.layers import assert_layer_factory
from ...layers import text_layer
from ...viewport import Viewport

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

	def test_fixed_text_layer(self):
		"""Tests fixed text layers.

		Also ensures that LiveText objects are updated.
		"""
		self.graphic = Text('text')
		self.viewport = Viewport(0, 0, 100, 100)
		self.offset_x = 10
		self.offset_y = 5

		# Test a static text layer first
		self.layer = text_layer.FixedStaticTextLayer(
			self.graphic, viewport=self.viewport,
			offset_x=self.offset_x, offset_y=self.offset_y
		)

		self.assert_layer_graphic_position()

		self.viewport.x = 10
		self.viewport.y = 10
		self.layer.update(0)

		self.assert_layer_graphic_position()

		self.viewport.x = 5
		self.viewport.y = 15
		self.layer.update(0)

		self.assert_layer_graphic_position()

		# Test a non-static text layer

		# We'll change the value of i and check if the text label is up to date
		self.i = 0
		self.graphic = LiveText(lambda: str(self.i))
		self.viewport = Viewport(0, 0, 100, 100)

		self.layer = text_layer.FixedTextLayer(
			self.graphic, viewport=self.viewport,
			offset_x=self.offset_x, offset_y=self.offset_y
		)

		self.assert_layer_graphic_position()
		self.assertEqual(self.layer.graphic.text, str(self.i),
			"Layer failed to update text layer.")

		self.viewport.x = 10
		self.viewport.y = 10
		self.i += 1
		self.layer.update(0)

		self.assert_layer_graphic_position()
		self.assertEqual(self.layer.graphic.text, str(self.i),
			"Layer failed to update text layer.")

		self.viewport.x = 5
		self.viewport.y = 15
		self.i += 1
		self.layer.update(0)
		self.assertEqual(self.layer.graphic.text, str(self.i),
			"Layer failed to update text layer.")

		self.assert_layer_graphic_position()

	def assert_layer_graphic_position(self):
		"""Asserts that the layer's graphic is at the expected coordinates."""
		expected_x = self.offset_x + self.viewport.x
		expected_y = self.offset_y + self.viewport.y
		graphic = self.layer.graphic

		self.assertEqual(graphic.x, expected_x,
			"x of layer graphic is %s, should be %s." % (graphic.x, expected_x))
		self.assertEqual(graphic.y, expected_y,
			"y of layer graphic is %s, should be %s." % (graphic.y, expected_y))
