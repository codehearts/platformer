from sys import modules

def get_property_from_string(property_value):
	"""Returns the value of the property represented by the given string.

	Args:
		property_value (str): The string representation of the property value to return.

	Returns:
		The value of the property represented by the string.
	"""
	split = property_value.rfind('.')
	module_name = property_value[ : split]
	property_name = property_value[split + 1 : ]

	return getattr(modules[module_name], property_name)
