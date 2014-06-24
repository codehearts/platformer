import os
import glob

# Dictionary of tags and translation functions to apply to config data values
installed_translators = {}
installed_translators_post = {} # For post-processing

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

def enable_post_processing():
	"""Enables post-processing translators."""
	global installed_translators

	installed_translators = dict(installed_translators.items() + installed_translators_post.items())
	"""
	Python 3:
	installed_translators = dict(installed_translators.items() + installed_translators_post.items())
	"""

def disable_post_processing():
	"""Disables post-processing translators."""
	global installed_translators

	for translator in installed_translators_post.keys():
		del installed_translators[translator]

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
			if tag in installed_translators:
				translated_data_value = installed_translators[tag](data_value[rightmost_tag_suffix+len(_data_value_tag_suffix):])

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

# Get all files not beginning with an underscore and import them
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if not os.path.basename(f).startswith('_')]
from . import *
