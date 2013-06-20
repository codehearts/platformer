import unittest
from pyglet.sprite import Sprite
from ..util.image import dummy_image
from ..util.layers import assert_layer_factory
from ...layers import graphics_layer
from ...physical_objects.physical_object import PhysicalObject
from ...viewport import Viewport

class TestGraphicsLayer(unittest.TestCase):
	"""Tests the base layer class."""

	def setUp(self):
		self.graphic = None
		self.viewport = None
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


	def test_fixed_graphics_layer(self):
		"""Tests fixed graphics layers."""
		self.graphic = Sprite(dummy_image(3, 4))
		self.viewport = Viewport(0, 0, 100, 100)
		self.offset_x = 10
		self.offset_y = 5

		# Test a static graphics layer first
		self.layer = graphics_layer.FixedStaticGraphicsLayer(
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

		# Test a non-static graphics layer
		stage = [[0]]
		self.graphic = PhysicalObject(stage, dummy_image(3, 4))
		self.viewport = Viewport(0, 0, 100, 100)

		self.layer = graphics_layer.FixedGraphicsLayer(
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

	def assert_layer_graphic_position(self):
		"""Asserts that the layer's graphic is at the expected coordinates."""
		expected_x = self.offset_x + self.viewport.x
		expected_y = self.offset_y + self.viewport.y
		graphic = self.layer.graphic

		self.assertEqual(graphic.x, expected_x,
			"x of layer graphic is %s, should be %s." % (graphic.x, expected_x))
		self.assertEqual(graphic.y, expected_y,
			"y of layer graphic is %s, should be %s." % (graphic.y, expected_y))
