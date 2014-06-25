import unittest
from ..load.config_translators import install_translator, translate, enable_post_processing, disable_post_processing
from ..load.level import Level
from util import custom_tile_types, resource
from util.tileset import get_testing_tileset

class TestLoadLevel(unittest.TestCase):
	"""Tests loading a level from a config file."""

	@classmethod
	def setUpClass(cls):
		resource.setUp()

	@classmethod
	def tearDownClass(cls):
		resource.tearDown()

	def test_level_config_translators(self):
		"""Tests translators for level config data to ensure that data strings are being translated to the correct values."""

		# Install test translators
		test_a_suffix = '_a'
		test_b_suffix = '_b'
		test_c_suffix = '_c'
		install_translator('test_a', lambda x: x+test_a_suffix)
		install_translator('test_b', lambda x: x+test_b_suffix)
		# Post-processing translators
		install_translator('test_c', lambda x: x+test_c_suffix, post=True)


		# Test translating an untagged value
		expected_data_value = 'the_data'
		data_value = translate(expected_data_value)

		self.assertEqual(data_value, expected_data_value,
			"Failed to leave untagged data value alone.")

		# Test translating an untagged non-string value
		expected_data_value = {'a': 1, 'b': 2, 'c': 3}
		data_value = translate(expected_data_value)

		self.assertEqual(data_value, expected_data_value,
			"Failed to leave untagged non-string data value alone.")

		# Test translating a single value
		data_value = translate('::test_a::data')
		expected_data_value = 'data'+test_a_suffix

		self.assertEqual(data_value, expected_data_value,
			"Failed to translate data value with single tag.")

		# Test translating a chain of tags
		data_value = translate('::test_b::::test_a::data')
		expected_data_value = 'data'+test_a_suffix+test_b_suffix

		# Test translating a single value that contains the tag suffix
		self.assertEqual(data_value, expected_data_value,
			"Failed to translate data value with multiple tags.")

		data_value = translate('::test_a::the::value')
		expected_data_value = 'the::value'+test_a_suffix

		self.assertEqual(data_value, expected_data_value,
			"Failed to translate data value with single tag and tag suffix in data.")

		# Test translating a chain of tags that contains the tag suffix
		data_value = translate('::test_b::::test_a::the::value')
		expected_data_value = 'the::value'+test_a_suffix+test_b_suffix

		self.assertEqual(data_value, expected_data_value,
			"Failed to translate data value with multiple tags and tag suffix in data.")

		# Test translating a chain of tags where one tag is unregistered
		data_value = translate('::test_b::::unregistered::::test_a::the::value')
		expected_data_value = '::unregistered::the::value'+test_a_suffix+test_b_suffix

		self.assertEqual(data_value, expected_data_value,
			"Failed to translate data value with multiple tags and unregistered tag in data.")

		# Test translating a data value which contains iteratable items
		data_value = translate({
			'abc': '::test_a::a value',
			'::test_b::def': [
				'::test_b::list item 1',
				'::unregistered::list item 1',
			],
			'ghi': {
				'a': 1,
				'b': [1, 2, '::test_a::3'],
				'c': '::test_b::::test_a::the::value'
			}
		})
		expected_data_value = {
			'abc': 'a value'+test_a_suffix,
			'def'+test_b_suffix: [
				'list item 1'+test_b_suffix,
				'::unregistered::list item 1',
			],
			'ghi': {
				'a': 1,
				'b': [1, 2, '3'+test_a_suffix],
				'c': 'the::value'+test_a_suffix+test_b_suffix
			}
		}

		self.assertEqual(data_value, expected_data_value,
			"Failed to recursively translate data value with iteratable contents.")

		# Ensure that a new dict object is not created during translation
		the_dict = {}
		data_value = translate(the_dict)

		self.assertIs(data_value, the_dict,
			"Recursively translating data value changed dict in memory.")

		# Ensure that a new dict object is not created during translation,
		# and that the dict is translated as expected
		the_dict = {
			'abc': {
				'::test_a::': 1,
				'::test_b::': 2,
				'c': 3
			},
			'::test_b::def': '::unregistered::item::'
		}
		the_dict_dict = the_dict['abc']
		data_value = translate(the_dict)
		expected_data_value = {
			'abc': {
				test_a_suffix: 1,
				test_b_suffix: 2,
				'c': 3
			},
			'def'+test_b_suffix: '::unregistered::item::'
		}

		self.assertIs(data_value, the_dict,
			"Recursively translating data value changed dict in memory.")

		self.assertIs(data_value['abc'], the_dict_dict,
			"Recursively translating data value changed dict inside dict in memory.")

		self.assertEqual(data_value, expected_data_value,
			"Recursively translating data value did not change dict in memory, but did not translate.")

		# Ensure that a new list object is not created during translation
		the_list = []
		data_value = translate(the_list)

		self.assertIs(data_value, the_list,
			"Recursively translating data value changed list in memory.")

		# Ensure that a new list object is not created during translation,
		# and that the list is translated as expected
		the_list = ['1::test_a::', '2::test_b::', '3_c', [4,5,'::unregistered::6::7::']]
		the_list_list = the_list[3]
		data_value = translate(the_list)
		expected_data_value = ['1'+test_a_suffix, '2'+test_b_suffix, '3_c', [4,5,'::unregistered::6::7::']]

		self.assertIs(data_value, the_list,
			"Recursively translating data value changed list in memory.")

		self.assertIs(data_value[3], the_list_list,
			"Recursively translating data value changed list inside list in memory.")

		self.assertEqual(data_value, expected_data_value,
			"Recursively translating data value did not change list in memory, but did not translate.")

		# Ensure that a new enumerable object is not created during translation,
		# and that the enumerable object is translated as expected
		the_enumerable = {
			'abc': [
				'::test_a::',
				'::test_b::a',
				'a_b_c'
			],
			'::test_b::def': [
				'::test_b::',
				'::test_a::',
				{
					'a': 1,
					'b': 2,
					'::test_a::::test_b::': 3
				}
			],
		}
		the_enumerable_list = the_enumerable['abc']
		the_enumerable_list_2 = the_enumerable['::test_b::def']
		the_enumerable_list_2_dict = the_enumerable_list_2[2]
		data_value = translate(the_enumerable)
		expected_data_value = {
			'abc': [
				test_a_suffix,
				'a'+test_b_suffix,
				'a_b_c'
			],
			'def'+test_b_suffix: [
				test_b_suffix,
				test_a_suffix,
				{
					'a': 1,
					'b': 2,
					test_b_suffix+test_a_suffix: 3
				}
			],
		}

		self.assertIs(data_value, the_enumerable,
			"Recursively translating data value changed object in memory.")

		self.assertIs(data_value['abc'], the_enumerable_list,
			"Recursively translating data value changed list inside dict in memory.")

		self.assertIs(data_value['def'+test_b_suffix], the_enumerable_list_2,
			"Recursively translating data value changed list inside dict in memory.")

		self.assertIs(data_value['def'+test_b_suffix][2], the_enumerable_list_2_dict,
			"Recursively translating data value changed dict inside list inside dict in memory.")

		self.assertEqual(data_value, expected_data_value,
			"Recursively translating data value did not change object in memory, but did not translate.")

		# Test post-processing with the translator
		data_value = translate('::test_a::::test_c::data')
		expected_data_value = '::test_c::data'+test_a_suffix

		self.assertEqual(data_value, expected_data_value,
			"Post-processing tag was translated before post-processing.")

		enable_post_processing()

		data_value = translate(data_value)
		expected_data_value = 'data'+test_a_suffix+test_c_suffix

		self.assertEqual(data_value, expected_data_value,
			"Post-processing tag was not translated during post-processing.")

		disable_post_processing()

	def test_level_loader(self):
		"""Tests the level loader to assure that values are loaded correctly."""

		# Install test translators
		install_translator('testing_tileset', lambda x: get_testing_tileset(2,2))
		install_translator('testing_tilemap', lambda x: [[0,3,2],[2,3,0]])

		# Test layer graphic dependency testing when dependency is defined first
		level_data = {
			'title': 'test level',
			'camera_target': 'player',
			'layers': [
				{
					'title': 'stage',
					'graphic': {
						'type': 'tile map',
						'tileset': '::testing_tileset::',
						'value_map': '::testing_tilemap::',
					},
				},
				{
					'title': 'player',
					'graphic': {
						'type': 'player',
						'stage': '::layer_graphic_property::stage.tiles',
						'player_data': {
							'x': 0,
							'y': 0,
						},
					},
				},
			],
		}

		level = Level(level_data)

		# TODO Use the layer manager to access layers by name once that's implemented
		self.assertEqual(level.layers[0].graphic.tiles, level.layers[1].graphic.stage,
			"Level loader failed to give player layer the tiles from stage layer when stage layer was defined first.")

		# TODO Use the layer manager to access layers by name once that's implemented
		self.assertIs(level.layers[0].graphic.tiles, level.layers[1].graphic.stage,
			"Layer graphic property was cloned when giving player layer tiles from stage layer when stage layer was defined first.")

		# Test layer graphic dependency testing when dependency is defined second
		level_data = {
			'title': 'test level',
			'camera_target': 'player',
			'layers': [
				{
					'title': 'player',
					'graphic': {
						'type': 'player',
						'stage': '::layer_graphic_property::stage.tiles',
						'player_data': {
							'x': 0,
							'y': 0,
						},
					},
				},
				{
					'title': 'stage',
					'graphic': {
						'type': 'tile map',
						'tileset': '::testing_tileset::',
						'value_map': '::testing_tilemap::',
					},
				},
			],
		}

		level = Level(level_data)

		# TODO Use the layer manager to access layers by name once that's implemented
		self.assertEqual(level.layers[0].graphic.tiles, level.layers[1].graphic.stage,
			"Level loader failed to give player layer the tiles from stage layer when stage layer was defined last.")

		# TODO Use the layer manager to access layers by name once that's implemented
		self.assertIs(level.layers[0].graphic.tiles, level.layers[1].graphic.stage,
			"Layer graphic property was cloned when giving player layer tiles from stage layer when stage layer was defined last.")

		# TODO Test script loading
