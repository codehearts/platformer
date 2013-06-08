from ...layers import create_from

def assert_layer_factory(self, layer_name):
	"""Asserts that the layer factory returns the expected classes for the graphics object.

	The instance running these assertions is expected to have ``graphic`` and ``expected_classes``
	attributes as follows:

	graphic (object): The graphics object for the layer.
	expected_classes (dict): A dict of the expected classes for each possible layer specification. The keys should include 'default', 'fixed', 'static', and 'static-fixed'. The values should be classes.

	Args:
		self (object): An instance of the test class running these assertions.
		layer_name (str): The name of the layer type (used for error output).
	"""
	# Default
	layer = create_from(self.graphic)

	self.assertEqual(type(layer), self.expected_classes['default'],
		"Layer factory failed to create proper "+layer_name+" layer with no specifications.")

	# Fixed
	layer = create_from(self.graphic, fixed=True)

	self.assertEqual(type(layer), self.expected_classes['fixed'],
		"Layer factory failed to create proper "+layer_name+" layer when specified as fixed.")

	# Static
	layer = create_from(self.graphic, static=True)

	self.assertEqual(type(layer), self.expected_classes['static'],
		"Layer factory failed to create proper "+layer_name+" layer when specified as static.")

	# Fixed and static
	layer = create_from(self.graphic, static=True, fixed=True)

	self.assertEqual(type(layer), self.expected_classes['static-fixed'],
		"Layer factory failed to create proper "+layer_name+" layer when specified as fixed and static.")
