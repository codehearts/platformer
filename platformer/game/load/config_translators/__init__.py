import os
import glob

# Dictionary of tags and translation functions to apply to config data values
installed_translators = {}
installed_translators_post = {} # For post-processing
enabled_translators = installed_translators # The translators that are currently enabled

# List of tests to confirm that a layer is ready for translation in post-processing
installed_translation_readiness_tests = []

_data_value_tag_prefix = '::'
_data_value_tag_suffix = '::'

def install_translator(data_type, translator, post=False):
	"""Adds support for translating data strings to other data types when loading
	a level config. All string values tagged with the given data type will be
	run through the given translator.

	Args:
		data_type (string): The name of the data type to add translation support for.
							This will be the tag to signify that a string should have
							the translator applied to it.
		translator (function): The function to apply to all tagged data values.

	Kwargs:
		post (bool): Whether or not the translator is intended for post-processing.
	"""
	global installed_translators, installed_translators_post

	if post:
		installed_translators_post[data_type] = translator
	else:
		installed_translators[data_type] = translator

def install_readiness_test(test_function):
	"""Adds the given test function to the list of tests to determine if a layer is ready
	for translation. The test function should accept the title of the layer to test.

	Args:
		test_function (function): The test function. This should accept the title of the
		                          layer as a string argument.
	"""
	global installed_translation_readiness_tests

	installed_translation_readiness_tests.append(translator)

def enable_post_processing():
	"""Enables post-processing translators."""
	global installed_translators_post, enabled_translators

	installed_translators_post = dict(installed_translators.items() + installed_translators_post.items())
	enabled_translators = installed_translators_post
	"""
	Python 3:
	installed_translators = dict(installed_translators.items() + installed_translators_post.items())
	"""

def disable_post_processing():
	"""Disables post-processing translators."""
	global enabled_translators

	enabled_translators = installed_translators

def translate(data_value, recurse=True):
	"""Translates tagged data values to other data types as specified by the tag.
	For example, '::property::a.b.c' will be translated into the `a.b.c` Python property.
	Tags are parsed from right to left to allow chaining, which is useful in cases such as
	'::image::::property::the.image.property'.

	Args:
		data_value (string): The data value string to translate. If the string contains no
							 tags, translation will not be performed.

	Kwargs:
		recurse (bool): Whether or not to recurse through the data value.

	Returns:
		The translated data value, which is of whatever type the translator returns.
	"""
	# If the data value is a string, it could contain a tag
	if isinstance(data_value, basestring):
		# Scan from the right, looking for tags in the left portion of the value
		right_bound = len(data_value)

		rightmost_tag_suffix = data_value.rfind(_data_value_tag_suffix, 0, right_bound)
		rightmost_tag_prefix = data_value.rfind(_data_value_tag_prefix, 0, rightmost_tag_suffix)
		while rightmost_tag_suffix != -1 and rightmost_tag_prefix != -1:
			tag = data_value[rightmost_tag_prefix+len(_data_value_tag_prefix) : rightmost_tag_suffix]
			if tag in enabled_translators:
				translated_data_value = enabled_translators[tag](data_value[rightmost_tag_suffix+len(_data_value_tag_suffix):])

				# The data value can't contain a tag anymore
				if not isinstance(translated_data_value, basestring):
					return translated_data_value
				else:
					data_value = data_value[:rightmost_tag_prefix] + translated_data_value
			else:
				# Skip over this occurence of the tag suffix
				right_bound = rightmost_tag_suffix

			rightmost_tag_suffix = data_value.rfind(_data_value_tag_suffix, 0, right_bound)
			rightmost_tag_prefix = data_value.rfind(_data_value_tag_prefix, 0, rightmost_tag_suffix)
	elif recurse:
		if isinstance(data_value, list):
			# Using [:] will update the contents of the list without creating a new list
			data_value[:] = map(translate, data_value)
		elif 'iteritems' in dir(data_value):
			# Using a for loop instead of map() to keep the object at the same place in memory
			for k, v in data_value.iteritems():
				translated_k = translate(k)

				data_value[translated_k] = translate(v)

				if translated_k != k:
					del data_value[k]

	return data_value

def ready_for_translation(layer_title):
	"""Returns True if the given layer is ready for translation.
	This can only be done during post-processing.
	"""
	# Reduces the tests list to the result of `True and test1(layer_title) and test2(layer_title) and ...`
	return reduce(lambda status,test: status and test(layer_title), installed_translation_readiness_tests, True)

# Get all files not beginning with an underscore and import them
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_')]
from . import *
