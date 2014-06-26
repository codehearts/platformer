import unittest
from util import dummy_graphics_module
from ..graphics import create_graphics_object
from ..graphics.installed_graphics import install_graphics_module

class TestGraphicsFactory(unittest.TestCase):

	def test_graphics_instantiation(self):
		"""Tests the installation graphics modules and instantiation of graphics objects."""

		name = 'Test Graphic'
		desc = 'A graphic for tests.'
		try:
			self.assertRaises(
				ValueError,
				create_graphics_object,
				dummy_graphics_module.recognized_name,
				name,
				desc=desc
			)
		except AssertionError:
			raise AssertionError('Graphics object factory did not raise ValueError when passed invalid module name.')

		try:
			install_graphics_module(
				dummy_graphics_module.__name__
			)
		except AssertionError:
			raise AssertionError('Failed to install dummy graphics module.')

		try:
			graphic = create_graphics_object(
				dummy_graphics_module.recognized_name,
				name,
				desc=desc
			)
		except AssertionError:
			raise AssertionError('Failed to create graphics object from recognized name.')

		self.assertTrue(
			isinstance(
				graphic,
				dummy_graphics_module.DummyGraphics
			),
			"Graphics factory failed to create object of the correct class.")

		self.assertEqual(graphic.name, name,
			"Graphics factory failed to initialize the graphics object with the given arguments.")

		self.assertEqual(graphic.desc, desc,
			"Graphics factory failed to initialize the graphics object with the given keyword arguments.")
