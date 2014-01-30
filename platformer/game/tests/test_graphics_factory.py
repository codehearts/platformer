import unittest
from util import dummy_graphics_module
from ..graphics import install_graphics_module, create_graphics_object

class TestGraphicsFactory(unittest.TestCase):

	def setUp(self):
		self.graphic = None

	def test_graphics_installation(self):
		"""Tests the installation of graphics modules."""

		self.graphic = None

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
                    self.graphic = create_graphics_object(
                        dummy_graphics_module.recognized_name,
                        name,
                        desc=desc
                    )
                except AssertionError:
                    raise AssertionError('Failed to create graphics object from recognized name.')

                self.assertTrue(
                    isinstance(
                        self.graphic,
                        dummy_graphics_module.DummyGraphics
                    ),
                    "Graphics factory failed to create object of the correct class.")

		self.assertEqual(self.graphic.name, name,
                    "Graphics factory failed to initialize the graphics object with the given arguments.")

		self.assertEqual(self.graphic.desc, desc,
                    "Graphics factory failed to initialize the graphics object with the given keyword arguments.")
