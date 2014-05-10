from game import util
from ..physical_objects import player
from ..resources import player_sprite
from ..settings import player_settings

# TODO This should return the actual player object, not act as a wrapper for it
class Player():

        def __init__(self, player_data, stage, key_handler=None):
                # Gather player data and settings to initiate with
                coordinates = util.tile_to_coordinate(player_data['x'], player_data['y'])
                player_data = {
                        'stage': stage,
                        'mass': player_settings.MASS,
                        'img': player_sprite.standing,
                        'x': coordinates[0],
                        'y': coordinates[1],
                        'key_handler': key_handler,
                }

                # Initiate the player
                self.character = player.Player(**player_data)

        # Update the player
        def update(self, dt):
                self.character.update(dt)

        # Draw the player to the screen
        def draw(self):
                self.batch.draw()
