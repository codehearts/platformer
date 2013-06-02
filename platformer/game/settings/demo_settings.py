# Demo stage data

TILE_DATA = {
# TODO Call this level-title or something
    'name': 'Demo Stage',
# TODO Call this tile-file or something
    'file': 'tilesets/demo/tiles.png',
#TODO Call this background-image
    'background': 'sky.png',
# TODO Find a more descriptive name for this
    'size': (20, 20),
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
