import game

def get_player_dash_percentage():
	# TODO level.layers[2] is a temporary way of getting the player layer
    player = game.level.layers[2].graphic
    return str(int((player.max_dash_time - player.time_dashed) / player.max_dash_time * 100))
