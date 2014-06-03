import unittest
from ..load.installed_level_config_translators import install_level_config_translator, translate_data_value
from ..load.level import Level

class TestLoadLevel(unittest.TestCase):
    """Tests loading a level from a config file."""

    def test_level_config_translators(self):
        """Tests translators for level config data to ensure that
        data strings are being translated to the correct values."""

        # Install test translators
        test_a_suffix = '_a'
        test_b_suffix = '_b'
        install_level_config_translator('test_a', lambda x: x+test_a_suffix)
        install_level_config_translator('test_b', lambda x: x+test_b_suffix)


        # Test translating an untagged value
        expected_data_value = 'the_data'
        data_value = translate_data_value(expected_data_value)

        self.assertEqual(data_value, expected_data_value,
            "Failed to leave untagged data value alone.")

        # Test translating an untagged non-string value
        expected_data_value = {'a': 1, 'b': 2, 'c': 3}
        data_value = translate_data_value(expected_data_value)

        self.assertEqual(data_value, expected_data_value,
            "Failed to leave untagged non-string data value alone.")

        # Test translating a single value
        data_value = translate_data_value('::test_a::data')
        expected_data_value = 'data'+test_a_suffix

        self.assertEqual(data_value, expected_data_value,
            "Failed to translate data value with single tag.")

        # Test translating a chain of tags
        data_value = translate_data_value('::test_b::::test_a::data')
        expected_data_value = 'data'+test_a_suffix+test_b_suffix

        # Test translating a single value that contains the tag suffix
        self.assertEqual(data_value, expected_data_value,
            "Failed to translate data value with multiple tags.")

        data_value = translate_data_value('::test_a::the::value')
        expected_data_value = 'the::value'+test_a_suffix

        self.assertEqual(data_value, expected_data_value,
            "Failed to translate data value with single tag and tag suffix in data.")

        # Test translating a chain of tags that contains the tag suffix
        data_value = translate_data_value('::test_b::::test_a::the::value')
        expected_data_value = 'the::value'+test_a_suffix+test_b_suffix

        self.assertEqual(data_value, expected_data_value,
            "Failed to translate data value with multiple tags and tag suffix in data.")
