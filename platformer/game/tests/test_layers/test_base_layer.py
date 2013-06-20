import unittest
import pyglet.app
from pyglet.clock import schedule_once
from ..util.layers import assert_layer_factory
from ...layers import base_layer

class TestBaseLayer(unittest.TestCase):
	"""Tests the base layer class."""

	def setUp(self):
		self.graphic = None
		self.layer = None

	expected_classes = {
		'default': base_layer.BaseLayer,
		'fixed': base_layer.BaseLayer,
		'static': base_layer.BaseLayer,
		'static-fixed': base_layer.BaseLayer,
	}

	def test_layer_factory(self):
		"""Tests the creation of a base layer via the layer factory."""
		assert_layer_factory(self, 'base')



	def test_layer_events(self):
		"""Tests base layer events."""
		schedule_once(self.run_layer_events_tests, 0)
		pyglet.app.run()

	def run_layer_events_tests(self, dt):
		"""Runs base layer event tests.

		These tests run for a significant amount of time
		in order to test for events being fired when the duration
		of the layer expires.

		Intended for use within a running pyglet app.
		``pyglet.app.run()`` should be called before calling this.
		"""

		# Test on_delete when delete() is called explicitly

		self.layer = base_layer.BaseLayer(None)

		self.layer_deletion_fired = False
		self.layer.set_handler(
			'on_delete', self.deletion_handler
		)

		self.layer.delete()

		self.assertTrue(self.layer_deletion_fired,
			"on_delete event did not fire when layer was deleted.")

		# Test on_delete event after layer duration has ended

		# Reset the layer's on_delete status
		self.layer_deletion_fired = False

		self.layer = base_layer.BaseLayer(None, duration=0.1)

		schedule_once(
			lambda layer: self.assertFalse(self.layer_deletion_fired,
				"on_delete event fired before layer duration was over."),
			0.05
		)

		schedule_once(
			lambda layer: self.assertFalse(self.layer_deletion_fired,
				"on_delete event did not fire when layer duration ended."),
			0.1
		)

		self.assertFalse(self.layer_deletion_fired,
			"on_delete event fired immediately after layer was created with duration.")

		schedule_once(lambda layer: pyglet.app.exit(), 0.15)

	def deletion_handler(self, layer):
		"""Handles an ``on_delete`` event from the layer."""
		self.layer_deletion_fired = True
