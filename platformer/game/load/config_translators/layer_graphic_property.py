from game.layers.level_config_translators import _layer_dependencies_met, _register_layer_graphic_dependency, _get_layer_graphic_property
from . import install_translator, install_readiness_test

# Add support for registering layer graphic dependencies
install_translator('layer_graphic_property', _register_layer_graphic_dependency)

# Resolve layer graphic dependencies during post-processing
install_translator('resolve_layer_graphic_dependency', _get_layer_graphic_property, post=True)

# Ensure a layer's graphic dependencies are met before post-processing translation
install_readiness_test(_layer_dependencies_met)
