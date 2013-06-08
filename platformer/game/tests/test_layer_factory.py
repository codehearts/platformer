import unittest
from ..layers import create_from
from ..layers.base_layer import BaseLayer

class TestLayerFactory(unittest.TestCase):

	def setUp(self):
		self.graphic = None
		self.layer = None

	def test_default_layer(self):
		"""Tests the creation of a default layer object."""
		self.graphic = None
		self.layer = create_from(self.graphic)

		self.assertEqual(type(self.layer), BaseLayer,
			"Layer factory failed to create default layer with no graphic.")

		self.layer = create_from(self.graphic, static=True, fixed=True)

		self.assertEqual(type(self.layer), BaseLayer,
			"Layer factory failed to create default layer with no graphic and inapplicable layer specifications.")
