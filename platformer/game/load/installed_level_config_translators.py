# Dictionary of tags and translation functions to apply to config data values
installed_translators = {}
_data_value_tag_prefix = ''
_data_value_tag_suffix = '::'

def install_level_config_translator(data_type, translator):
    """Adds support for translating data strings to other data types when loading
    a level config. All string values tagged with the given data type will be
    run through the given translator.

    Args:
        data_type (string): The name of the data type to add translation support for.
                            This will be the tag to signify that a string should have
                            the translator applied to it.
        translator (function): The function to apply to all tagged data values.
    """
    global installed_translators, _data_value_tag_prefix, _data_value_tag_suffix
    installed_translators[_data_value_tag_prefix + data_type + _data_value_tag_suffix] = translator
