import texture_tile_map_layer
import tile_map_layer
import text_layer
import animation_layer
import graphics_layer
import image_layer

installed_layers = []
def install_layer(layer_module):
	global installed_layers

	installed_layers.append({
		'recognizer': layer_module.recognizer,
		'factory': layer_module.factory,
	})

# Before TileMapLayer because TextureTileMap is more specific
install_layer(texture_tile_map_layer)
install_layer(tile_map_layer)
install_layer(text_layer)
install_layer(animation_layer)

# GraphicsLayer before ImageLayer because graphics can support blitting
install_layer(graphics_layer)
install_layer(image_layer)
