from slope_tile import slope_tile_factory

"""Dictionary of custom tile types and their factory methods.

The keys should be the name of the tile type, and the value should be
a callback method for returning the appropriate tile object from any
provided arguments.
"""
custom_tile_types = {
	'slope': slope_tile_factory,
}
