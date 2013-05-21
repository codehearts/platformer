from ..settings import tile_settings

# Demo stage data

TILE_DATA = {
# TODO Call this level-title or something
    'name': 'Demo Stage',
# TODO Call this tile-file or something
    'file': 'demo-tiles.png',
#TODO Call this background-image
    'background': 'sky.png',
# TODO Find a more descriptive name for this
    'size': (20, 20),
# TODO Find a better name for this
    'key': {
        tile_settings.RIGHT_SLOPE_1:	[9],
        tile_settings.LEFT_SLOPE_1:		[10],
        tile_settings.RIGHT_SLOPE_2_1:	[13],
        tile_settings.RIGHT_SLOPE_2_2:	[14],
        tile_settings.LEFT_SLOPE_2_1:	[15],
        tile_settings.LEFT_SLOPE_2_2:	[16],
        tile_settings.TOP_LEFT_SLOPE_1:	[18]
    },
    'events': {
        'player_events': [
            {
                'run': 'once',
                'condition': lambda player: player.tile_x >= 25,
                'function': 'demo_stage_1'
            }
        ]
    }
}
