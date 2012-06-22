from ..settings import tile_settings

# Demo stage data

TILE_DATA = {
    'name': 'Demo Stage',
    'file': 'demo-tiles.png',
    'background': 'sky.png',
    'size': (20, 20),
    'key': {
        tile_settings.RIGHT_SLOPE_1:   [9],
        tile_settings.LEFT_SLOPE_1:    [10],
        tile_settings.RIGHT_SLOPE_2_1: [13],
        tile_settings.RIGHT_SLOPE_2_2: [14],
        tile_settings.LEFT_SLOPE_2_1:  [15],
        tile_settings.LEFT_SLOPE_2_2:  [16],
        tile_settings.TOP_LEFT_SLOPE_1:    [18]
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