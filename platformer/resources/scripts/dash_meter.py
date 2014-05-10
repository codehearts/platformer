import game

def get_player_dash_percentage():
    player = game.level.layer_dict['player'].graphic
    return str(int((player.max_dash_time - player.time_dashed) / player.max_dash_time * 100))
